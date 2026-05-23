import sys
import os
import subprocess

def main():
    # Ensure UTF-8 console output for beautiful ASCII art
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    current_dir = os.path.dirname(os.path.abspath(__file__))
    cli_script = os.path.join(current_dir, "saga_cli.py")
    
    # We forward execution to the unified SAGA --init engine
    args = [sys.executable, cli_script, "--init"]
    
    # Forward the first argument as target directory if provided
    # e.g., if user runs: python start_new_book.py target-book
    if len(sys.argv) > 1:
        # Check if the user is passing argparse-style flags or a raw name
        target = sys.argv[1]
        if not target.startswith("-"):
            args.append(target)
            
    print("✨ SAGA WRITING DESK CREATION WIZARD ✨")
    print("---------------------------------------")
    print("Routing configuration process through the SAGA unified core engine...")
    
    try:
        subprocess.run(args, check=True)
    except KeyboardInterrupt:
        print("\n\n⚠️ Onboarding wizard interrupted by user. Exit.")
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)
    except Exception as e:
        print(f"❌ Error invoking SAGA core: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
