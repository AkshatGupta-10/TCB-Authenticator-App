{
	'name': 'TCB Subscription App',
	'summary': 'TCB Subscription app',
	'category': 'Security',
	'author': 'Akshat Gupta',
	'maintainer': 'Akshat Gupta',
	'company': 'TCB Infotech',
	'website': 'https://www.tcbinfotech.com',
	'depends': ['base','base_setup'],
	'data': [
		'security/ir.model.access.csv',
        'views/tcb_subscription_views.xml',
		'views/authenticator_app_views.xml',
		# 'views/setting_addons_views.xml',
	],
	'installable': True,
	'application': True,
	'auto_install': False,
}