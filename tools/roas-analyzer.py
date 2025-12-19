"""Calculate ROAS for a list of conversions."""

def calculate_roas(spend, revenue):
    if spend == 0:
        return 0
    return (revenue / spend) * 100


if __name__ == '__main__':
    spend = 3000
    revenue = 15000
    print(f"ROAS: {calculate_roas(spend, revenue):.2f}%")
