import os
import django
from django.contrib.auth.models import User, Group

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Utwórz grupę Manager jeśli nie istnieje
manager_group, created = Group.objects.get_or_create(name='Manager')
if created:
    print(f"✅ Grupa 'Manager' utworzona")
else:
    print(f"✅ Grupa 'Manager' już istnieje")

# Utwórz superusera jeśli nie istnieje
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )
    print("✅ Superuser 'admin' / 'admin123' utworzony")
else:
    print("✅ Superuser 'admin' już istnieje")

# Utwórz przykładowego pracownika
if not User.objects.filter(username='john').exists():
    user = User.objects.create_user(
        username='john',
        email='john@example.com',
        password='john123'
    )
    print("✅ Użytkownik 'john' / 'john123' utworzony")
else:
    print("✅ Użytkownik 'john' już istnieje")

# Utwórz przykładowego szefa
if not User.objects.filter(username='boss').exists():
    boss = User.objects.create_user(
        username='boss',
        email='boss@example.com',
        password='boss123'
    )
    boss.groups.add(manager_group)
    boss.save()
    print("✅ Szef 'boss' / 'boss123' utworzony (w grupie Manager)")
else:
    print("✅ Szef 'boss' już istnieje")

print("\n✅ Baza danych jest gotowa!")
print("\nDostępni użytkownicy:")
print("  Admin:     admin / admin123")
print("  Pracownik: john / john123")
print("  Szef:      boss / boss123")
