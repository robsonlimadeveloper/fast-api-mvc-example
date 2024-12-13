from app.seeds.seed_user import seeds as user_seed
from sqlalchemy.orm import Session
from app.modules import get_models
from sqlalchemy import func, text

class Seeds:
    """This class runs seeds"""
    def __init__(self, db: Session, modules):
        self.session: Session = db
        self.models = get_models()

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
            print(f"Error synchronizing sequences: {error}")
            self.session.rollback()
            raise

    def run(self):
        """This method runs seeds"""
        
        # Check if admin user exists
        try:
            admin_user = self.session.query(self.models["User"]).filter_by(username="admin").first()
            if admin_user:
                print("Admin user already exists. Skipping seed.")
                return
        except Exception as error:
            print(f"Error checking admin user: {error}")
        
        user = self.models["User"]

        try:
            print("Getting Started with First Seeds...")
            
            # Generate seed data
            users = user_seed(user)
            self.session.add_all(users)

            print("Successfully inserted data from First Seed.")
        except Exception as error:
            self.session.rollback()
            print(f"Error inserting seed data: {error}")
            raise
        else:
            self.session.commit()
        finally:
            self.session.close()

        self.synchronize_sequences()
