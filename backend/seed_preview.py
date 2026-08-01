import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal, engine
from app.models.user import User
from app.models.booking import Garage, Booking
from app.models.vehicle import Vehicle, Inspection
from app.core.security import get_password_hash
from sqlalchemy.future import select

async def seed_preview_data():
    async with AsyncSessionLocal() as db:
        # Get a garage to assign to the mechanic
        result = await db.execute(select(Garage).where(Garage.name == "Mike's Auto Body"))
        garage = result.scalars().first()
        
        if not garage:
            print("Garage not found. Make sure you have fetched garages via the API to trigger auto-seeding.")
            # Auto-seed Mike's just in case
            garage = Garage(name="Mike's Auto Body", address="123 Main St", latitude=37.77, longitude=-122.41, phone="555-0101")
            db.add(garage)
            await db.commit()
            await db.refresh(garage)

        # Check if test mechanic exists
        result = await db.execute(select(User).where(User.email == "mechanic@automediai.com"))
        mechanic = result.scalars().first()
        
        if not mechanic:
            print("Creating test mechanic account...")
            mechanic = User(
                email="mechanic@automediai.com",
                full_name="Mike (Mechanic)",
                hashed_password=get_password_hash("password123"),
                role="mechanic",
                garage_id=garage.id
            )
            db.add(mechanic)
            await db.commit()
            print(f"Success! Created mechanic account.")
            print(f"Email: mechanic@automediai.com")
            print(f"Password: password123")
            print(f"Garage: {garage.name}")
        else:
            print("Test mechanic already exists.")
            # Ensure garage is linked
            if mechanic.garage_id != garage.id:
                mechanic.garage_id = garage.id
                await db.commit()
                print("Updated existing mechanic to link with Mike's Auto Body.")
            
        # Check if there are bookings for Mike's Auto Body
        from app.models.booking import Booking
        from datetime import datetime, timedelta
        result = await db.execute(select(Booking).where(Booking.garage_id == garage.id))
        bookings = result.scalars().all()
        if not bookings:
            print("Seeding test bookings for Mike's Auto Body...")
            b1 = Booking(user_id=1, garage_id=garage.id, appointment_time=datetime.now() + timedelta(days=1), status='pending')
            b2 = Booking(user_id=1, garage_id=garage.id, appointment_time=datetime.now() - timedelta(days=1), status='confirmed')
            db.add(b1)
            db.add(b2)
            await db.commit()
            print("Successfully seeded test bookings.")

if __name__ == "__main__":
    asyncio.run(seed_preview_data())
