from app.core.database import SessionLocal
from app.repositories import RoleRepository

ROLES = [
    (
        "admin",
        "Platform Administrator",
    ),
    (
        "analyst",
        "Security Analyst",
    ),
    (
        "viewer",
        "Read Only User",
    ),
]


def main():
    db = SessionLocal()

    repository = RoleRepository(db)

    for name, description in ROLES:
        if repository.get_by_name(name):
            continue

        repository.create(
            name=name,
            description=description,
        )

    print("Roles seeded successfully.")

    db.close()


if __name__ == "__main__":
    main()
