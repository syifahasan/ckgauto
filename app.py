from src.runners.run_registration import run_registration
from src.runners.run_service import run_service
from src.runners.run_confirmation import run_confirmation

if __name__ == "__main__":
    mode = "registration"  # Change this to "service" or "confirmation" as needed

    if mode == "registration":
        run_registration()
    elif mode == "service":
        run_service()
    elif mode == "confirmation":
        run_confirmation()