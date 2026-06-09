import bcrypt

users = [
    ("admin_ford_pines", "admin123", 1),
    ("admin_grunkle_stan", "admin123", 1),

    ("lec_eda_clawthorne", "lecturer123", 2),
    ("lec_queen_moon", "lecturer123", 2),
    ("lec_alador_blight", "lecturer123", 2),

    ("stu_marinette_dupain", "student123", 3),
    ("stu_adrien_agreste", "student123", 3),
    ("stu_alya_cesaire", "student123", 3),
    ("stu_nino_lahiffe", "student123", 3),
    ("stu_chloe_bourgeois", "student123", 3),

    ("stu_dipper_pines", "student123", 3),
    ("stu_mabel_pines", "student123", 3),
    ("stu_wendy_corduroy", "student123", 3),

    ("stu_twilight_sparkle", "student123", 3),
    ("stu_rainbow_dash", "student123", 3),
    ("stu_rarity", "student123", 3),
    ("stu_applejack", "student123", 3),
    ("stu_fluttershy", "student123", 3),
    ("stu_pinkie_pie", "student123", 3),
    ("stu_sunset_shimmer", "student123", 3),

    ("stu_luz_noceda", "student123", 3),
    ("stu_amity_blight", "student123", 3),
    ("stu_willow_park", "student123", 3),
    ("stu_gus_porter", "student123", 3),
    ("stu_hunter", "student123", 3),

    ("stu_star_butterfly", "student123", 3),
    ("stu_marco_diaz", "student123", 3),
    ("stu_janna_ordonia", "student123", 3),
    ("stu_starfan13", "student123", 3),
]

print("INSERT INTO users (username, password, role_id) VALUES")

rows = []
for username, password, role_id in users:
    hashed = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    rows.append(
        f"('{username}', '{hashed}', {role_id})"
    )

print(",\n".join(rows) + ";")