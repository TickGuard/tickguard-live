def calculate_risk(latitude: float, longitude: float, month: int) -> float:
    """
    Updated TickGuard risk engine with:
    - Corrected August seasonality
    - Blacklegged + Lone Star tick curves
    - Region-based species weighting
    - Increased regional baseline weighting
    """

    # -----------------------------
    # 1. Seasonality curves
    # -----------------------------

    blacklegged = {
        1: 0.10, 2: 0.10, 3: 0.20,
        4: 0.50, 5: 0.80, 6: 1.00,
        7: 0.90, 8: 0.60,   # Corrected August
        9: 0.40, 10: 0.60,
        11: 0.70, 12: 0.50
    }

    lone_star = {
        1: 0.05, 2: 0.10, 3: 0.20,
        4: 0.50, 5: 0.70, 6: 0.90,
        7: 1.00, 8: 1.00,   # Lone Star peak includes August
        9: 0.70, 10: 0.40,
        11: 0.20, 12: 0.10
    }

    # -----------------------------
    # 2. Region-based species weighting
    # -----------------------------

    def species_weights(lat, lon):
        # Northeast (CT, MA, RI, NY, NJ, PA)
        if lat > 40 and lon < -70 and lon > -80:
            return 0.9, 0.1

        # Mid-Atlantic (MD, VA, DE)
        if 36 < lat < 40 and -80 < lon < -74:
            return 0.6, 0.4

        # Upper Midwest (WI, MN, MI)
        if lat > 42 and lon < -85:
            return 0.8, 0.2

        # Southeast (TN, KY, NC, SC, GA, AR, MO)
        if 32 < lat < 40 and lon < -75:
            return 0.2, 0.8

        return 0.7, 0.3

    w_black, w_lone = species_weights(latitude, longitude)

    seasonality = (
        blacklegged[month] * w_black +
        lone_star[month] * w_lone
    )

    # -----------------------------
    # 3. Regional baseline risk
    # -----------------------------

    def regional_baseline(lat, lon):
        # Northeast
        if lat > 40 and lon < -70 and lon > -80:
            return 0.85

        # Mid-Atlantic
        if 36 < lat < 40 and -80 < lon < -74:
            return 0.90

        # Upper Midwest
        if lat > 42 and lon < -85:
            return 0.80

        # Southeast (Lone Star heavy)
        if 32 < lat < 40 and lon < -75:
            return 0.75

        # West Coast
        if lon < -120:
            return 0.30

        # Mountain West
        if lon < -105:
            return 0.15

        return 0.40

    regional = regional_baseline(latitude, longitude)

    # -----------------------------
    # 4. Habitat suitability
    # -----------------------------

    def habitat(lat, lon):
        if lon > -95:
            return 0.7  # forest-heavy east
        if -105 < lon < -95:
            return 0.4  # plains
        return 0.2      # arid west

    habitat_factor = habitat(latitude, longitude)

    # -----------------------------
    # 5. Updated weighted formula
    # -----------------------------

    risk_score = (
        seasonality * 0.35 +
        regional * 0.45 +
        habitat_factor * 0.20
    )

    return max(0.0, min(1.0, risk_score))
