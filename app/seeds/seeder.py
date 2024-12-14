import os
import importlib
from app.core.logging import logger
from app.seeds.seed_user import seeds as user_seed
from sqlalchemy.orm import Session
from app.modules import get_models
from sqlalchemy import func, text
from app.config import (SessionLocal, engine, settings,
                        pwd_settings, Base, get_db)

class Seeds:
    """This class runs seeds"""
    def __init__(self, db: Session, modules):
        self.session: Session = db
        self.models = get_models()

    def register_models(self):
        """
        This method register models
        """
        modules_path = "app/modules"
        module_names = [
            module
            for module in os.listdir(modules_path)
            if os.path.isdir(os.path.join(modules_path, module)) and
            os.path.exists(os.path.join(modules_path, module, "model.py"))
        ]

        for module_name in module_names:
            import_path = f"app.modules.{module_name}.model"
            try:
                importlib.import_module(import_path)
            except Exception as e:
                logger.error(f"Failed to import {import_path}: {e}")


    def create_tables(self):
        """This method create tables"""
        Base.metadata.create_all(bind=engine)

    def synchronize_sequences(self):
        """Synchronize database sequences with the current maximum ID."""
        try:
            for model_name, model in self.models.items():
                
                if hasattr(model, '__table__') and model.__table__.columns:
                    
                    primary_key_column = next(
                        (column for column in model.__table__.columns if column.primary_key), None
                    )
                    
                    if primary_key_column is not None and primary_key_column.autoincrement:
                        
                        sequence_name = f"{model.__tablename__}_{primary_key_column.name}_seq"
                        
                        max_id = self.session.execute(
                            func.max(getattr(model, primary_key_column.name))
                        ).scalar() or 0  

                        self.session.execute(
                            text("SELECT setval(:seq_name, :new_value)"),
                            {"seq_name": sequence_name, "new_value": max_id}
                        )
            self.session.commit()
        except Exception as error:
            logger.error(f"Error synchronizing sequences: {error}")
            self.session.rollback()
            raise

    def run(self):
        """This method runs seeds"""
        
        # Check if admin user exists
        try:
            admin_user = self.session.query(self.models["User"]).filter_by(username="admin").first()
            if admin_user:
                logger.info("Skipping seeds data because admin user already exists.")
                return
        except Exception as error:
            logger.error(f"Error checking admin user: {error}")
        
        user = self.models["User"]

        try:
            logger.info("Getting Started with First Seeds...")
            
            # Generate seed data
            users = user_seed(user)
            self.session.add_all(users)

            logger.info("Successfully inserted data from First Seed.")
        except Exception as error:
            self.session.rollback()
            logger.error(f"Error inserting seed data: {error}")
            raise
        else:
            self.session.commit()
        finally:
            self.session.close()
