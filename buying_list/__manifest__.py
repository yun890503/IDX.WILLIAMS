{
    'name': 'group_buying',
    'version': '1.0',
    'summary': '模組簡介',
    'author': 'IDX.Williams',
    'category': 'Category',
    'depends': [
        'base',  # 基礎模組
        'mail',
        'purchase',   
    ],
    'data': [
        
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/group_buying_views.xml',
        'views/group_buying_menu.xml',
        'views/purchase_order_views.xml',
    ],
    'installable': True,
    'application': True,

    
}
