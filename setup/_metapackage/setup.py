import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-open-synergy-ssi-school-incident",
    description="Meta package for open-synergy-ssi-school-incident Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-ssi_school_incident',
        'odoo14-addon-ssi_school_incident_operating_unit',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
