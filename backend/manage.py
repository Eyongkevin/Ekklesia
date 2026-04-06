import typer
from getpass import getpass
from app.db.uow import UnitOfWork
from app.services.user import UserService
from app.services.membership import MembershipService

from app.core.utils import MembershipRole
from app.core.utils import hash_password

app = typer.Typer(help="Manage Ekklesia backend tasks")



@app.command()
def createsuperuser():
    """
    Create a SUPER_ADMIN user.
    """
    typer.echo("Create a new SUPER_ADMIN user")

    email = typer.prompt("Email").strip()
    password = getpass("Password: ").strip()
    confirm = getpass("Confirm Password: ").strip()

    if password != confirm:
        typer.echo("Passwords do not match!")
        raise typer.Exit(code=1)

    with UnitOfWork() as uow:
        user_service = UserService(uow)
        membership_service = MembershipService(uow)

        # Check if user exists
        existing_user = user_service.get_user_by_email(email)
        if existing_user:
            typer.echo("User with this email already exists.")
            raise typer.Exit(code=1)

        # Create user
        user = user_service.create_user(
            email=email,
            password=hash_password(password)
        )

        # Assign SUPER_ADMIN role
        membership_service.create_membership(
            user_id=str(user.id),
            role=MembershipRole.SUPER_ADMIN
        )

        typer.echo(f"SUPER ADMIN {email} created successfully.")


if __name__ == "__main__":
    app()