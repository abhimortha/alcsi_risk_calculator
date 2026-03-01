import numpy as np

def plco_m2012(
    age,
    race,
    education,
    bmi,
    copd,
    cancer_hist,
    family_hist_lung_cancer,
    smoking_status,
    smoking_intensity,
    duration_smoking,
    smoking_quit_time
):

    race = race.lower()

    # Base linear predictor
    model = (
        0.0778868 * (age - 62)
        - 0.0812744 * (education - 4)
        - 0.0274194 * (bmi - 27)
        + 0.3553063 * copd
        + 0.4589971 * cancer_hist
        + 0.587185 * family_hist_lung_cancer
        + 0.2597431 * smoking_status
        - 1.822606 * ((smoking_intensity / 10) ** (-1) - 0.4021541613)
        + 0.0317321 * (duration_smoking - 27)
        - 0.0308572 * (smoking_quit_time - 10)
        - 4.532506
    )

    # Race adjustments
    if race == "black":
        model += 0.3944778
    elif race == "hispanic":
        model -= 0.7434744
    elif race == "asian":
        model -= 0.466585
    elif race in ["native hawaiian", "pacific islander"]:
        model += 1.027152
    # White/American Indian/Alaskan Native → no change

    # Logistic transformation
    prob = np.exp(model) / (1 + np.exp(model))

    return prob
