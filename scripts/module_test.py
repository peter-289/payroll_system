from datetime import datetime 
def _generate_reference_number():
        """Generates a unique reference number for the allowance."""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
        
        return f"ALW-{timestamp}"

print(_generate_reference_number())

