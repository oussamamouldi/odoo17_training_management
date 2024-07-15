
{
    'name': "Gestion des formations",

    'summary': """
    Ce module est destiné pour gérer un centre de formation
""",

    'description': """Ce module est destiné pour gérer un centre de formation""",

    'author': "Mouldi Oussama",
    'website': "",


    'category': 'Formations',
    'version': '17.0.0.1.0',


    'depends': ['base'],


    'data': [
        'security/ir.model.access.csv',
        'views/formation.xml',

    ],
}