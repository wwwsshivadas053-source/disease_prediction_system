explanations = {
    "Melanoma": (
        "Melanoma is a high-risk skin cancer that starts in pigment-producing cells. "
        "It may appear as a new dark spot or an existing mole that changes in size, "
        "shape, color, border, or sensation. Because melanoma can spread faster than "
        "many other skin cancers, suspicious results need prompt clinical review."
    ),
    "Nevus": (
        "A nevus is a mole or pigmented skin growth. Most nevi are benign and remain "
        "stable for years, but a mole that becomes asymmetric, develops uneven borders, "
        "changes color, grows quickly, itches, bleeds, or looks different from nearby "
        "moles should be examined by a dermatologist."
    ),
    "Basal Cell Carcinoma": (
        "Basal cell carcinoma is a common skin cancer that often develops on sun-exposed "
        "areas such as the face, neck, scalp, or arms. It may look like a pearly bump, "
        "a pink patch, a shiny scar-like area, or a sore that repeatedly heals and opens. "
        "It usually grows slowly but can damage nearby tissue if untreated."
    ),
    "Actinic Keratosis": (
        "Actinic keratosis is a rough, dry, or scaly patch caused by long-term ultraviolet "
        "exposure. It is considered precancerous because a small percentage can progress "
        "to squamous cell carcinoma. It is common on the face, ears, scalp, lips, hands, "
        "and forearms."
    ),
    "Benign Keratosis": (
        "Benign keratosis describes non-cancerous growths such as seborrheic keratoses "
        "or similar lesions. They may look waxy, raised, rough, brown, gray, or stuck on "
        "the skin. They are usually harmless but can resemble more serious lesions in "
        "some images."
    ),
    "Dermatofibroma": (
        "Dermatofibroma is commonly a small, firm, benign skin nodule that may appear "
        "pink, brown, or reddish-brown. It is often linked to minor skin injury, insect "
        "bites, or irritation. It may feel hard and can dimple inward when gently pinched."
    ),
    "Vascular Lesion": (
        "A vascular lesion is related to blood vessels and may appear red, purple, blue, "
        "or dark. Examples include angiomas, blood-vessel malformations, or other vessel "
        "based marks. Many are benign, but fast growth, pain, ulceration, or bleeding "
        "should be checked."
    ),
    "Healthy": (
        "No significant visible abnormality was detected in the uploaded image. This does "
        "not replace a full skin examination, because image quality, lighting, angle, and "
        "hidden symptoms can affect AI interpretation."
    )
}

solutions = {
    "Melanoma": (
        "Arrange an urgent dermatology appointment for dermoscopy and possible biopsy. "
        "Avoid delaying care, do not try home removal, protect the area from sun exposure, "
        "and bring notes about when the lesion changed or first appeared."
    ),
    "Nevus": (
        "Monitor the mole using the ABCDE rule: asymmetry, border, color, diameter, and "
        "evolution. Photograph it monthly under similar lighting, use sun protection, and "
        "book a dermatology visit if it changes or looks unusual."
    ),
    "Basal Cell Carcinoma": (
        "Consult a dermatologist for confirmation and treatment planning. Common options "
        "may include excision, topical therapy, curettage, cryotherapy, or Mohs surgery, "
        "depending on the lesion site, size, and depth."
    ),
    "Actinic Keratosis": (
        "Schedule a skin check, reduce ultraviolet exposure, use broad-spectrum sunscreen, "
        "and wear protective clothing. A clinician may recommend cryotherapy, topical "
        "medicine, photodynamic therapy, or follow-up monitoring."
    ),
    "Benign Keratosis": (
        "Usually no urgent treatment is required. Seek medical review if it grows quickly, "
        "bleeds, becomes painful, changes color, or is difficult to distinguish from a mole "
        "or skin cancer. Removal can be discussed if it is irritated or cosmetic."
    ),
    "Dermatofibroma": (
        "Most dermatofibromas only need observation. Avoid scratching or repeated friction. "
        "See a clinician if the nodule enlarges rapidly, becomes painful, bleeds, changes "
        "color, or if the diagnosis is uncertain."
    ),
    "Vascular Lesion": (
        "Avoid trauma to the area and monitor for bleeding, pain, or fast growth. Consult a "
        "clinician if the lesion is new, enlarging, ulcerated, repeatedly bleeding, or located "
        "near sensitive areas such as the eye or lip."
    ),
    "Healthy": (
        "Continue regular skin self-checks, use sunscreen, avoid tanning, and seek medical "
        "advice if you notice a new, changing, painful, itchy, or bleeding lesion."
    )
}

disease_details = {
    "Melanoma": {
        "risk_level": "High priority",
        "common_signs": [
            "Irregular borders or asymmetric shape",
            "Multiple colors such as black, brown, red, blue, or white",
            "Rapid change, bleeding, itching, or new elevation"
        ],
        "care_focus": [
            "Urgent specialist review",
            "Dermoscopy and biopsy if clinically indicated",
            "Full-body skin check for related lesions"
        ]
    },
    "Nevus": {
        "risk_level": "Usually low, monitor changes",
        "common_signs": [
            "Stable brown or skin-colored mole",
            "Round or oval shape with regular borders",
            "No recent bleeding, pain, or fast growth"
        ],
        "care_focus": [
            "Monthly self-checks",
            "ABCDE monitoring",
            "Dermatology review for changing or unusual moles"
        ]
    },
    "Basal Cell Carcinoma": {
        "risk_level": "Needs clinical confirmation",
        "common_signs": [
            "Pearly or shiny bump",
            "Non-healing sore or recurring scab",
            "Pink patch or scar-like shiny area"
        ],
        "care_focus": [
            "Dermatology consultation",
            "Treatment before deeper local tissue damage",
            "Sun protection and follow-up checks"
        ]
    },
    "Actinic Keratosis": {
        "risk_level": "Precancerous potential",
        "common_signs": [
            "Rough, dry, or sandpaper-like patch",
            "Common on sun-exposed skin",
            "May sting, itch, or feel tender"
        ],
        "care_focus": [
            "Skin examination",
            "UV exposure reduction",
            "Treatment if persistent or widespread"
        ]
    },
    "Benign Keratosis": {
        "risk_level": "Usually benign",
        "common_signs": [
            "Waxy or stuck-on appearance",
            "Rough, raised, brown, gray, or tan surface",
            "Can become irritated by clothing or scratching"
        ],
        "care_focus": [
            "Observation if stable",
            "Review if bleeding or rapidly changing",
            "Optional removal for irritation or cosmetic reasons"
        ]
    },
    "Dermatofibroma": {
        "risk_level": "Usually benign",
        "common_signs": [
            "Firm small bump",
            "Pink, brown, or reddish-brown color",
            "Dimple sign when gently pinched"
        ],
        "care_focus": [
            "Observation",
            "Avoid repeated irritation",
            "Clinical review for pain, bleeding, or rapid growth"
        ]
    },
    "Vascular Lesion": {
        "risk_level": "Often benign, review if changing",
        "common_signs": [
            "Red, purple, blue, or dark vessel-based mark",
            "May blanch or bleed when irritated",
            "Can be flat or raised"
        ],
        "care_focus": [
            "Avoid scratching or trauma",
            "Monitor growth and bleeding",
            "Medical review for new or symptomatic lesions"
        ]
    },
    "Healthy": {
        "risk_level": "No visible concern detected",
        "common_signs": [
            "No obvious suspicious lesion in the uploaded image",
            "Even color and texture",
            "No visible ulceration or bleeding"
        ],
        "care_focus": [
            "Continue self-checks",
            "Use sun protection",
            "Seek care for new or changing symptoms"
        ]
    }
}

disease_cards = [
    {
        "name": disease,
        "summary": explanations[disease],
        "solution": solutions[disease],
        "risk_level": disease_details[disease]["risk_level"]
    }
    for disease in (
        "Melanoma",
        "Nevus",
        "Basal Cell Carcinoma",
        "Actinic Keratosis",
        "Benign Keratosis",
        "Dermatofibroma",
        "Vascular Lesion"
    )
]
