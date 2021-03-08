# -*- coding: utf-8 -*-

###################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2018-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Niyas Raphy(<https://www.cybrosys.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################

{
    'name': 'Res Partner Commercial Name',
    'summary': """Add the business name field in res_partner""",
    'version': '12.0.1.0.0',
    'description': """Add the business name field in res_partner""",
    'author': 'DDL',
    'company': 'Xtendoo',
    'website': 'http://www.xtendoo.es',
    'category': 'Extra Tools',
    'depends': [
        'base'
    ],
    'license': 'AGPL-3',
    'data': [
        'views/commercial_name.xml',
        'views/search_commercial_name.xml',
        'views/view_partner_tree_commercial_name.xml',
        'views/view_partner_kanban_commercial_name.xml'
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,

}
