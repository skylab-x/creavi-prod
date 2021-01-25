# -*- coding: utf-8 -*-
# from odoo import http


# class CreaviProducts(http.Controller):
#     @http.route('/creavi_products/creavi_products/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/creavi_products/creavi_products/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('creavi_products.listing', {
#             'root': '/creavi_products/creavi_products',
#             'objects': http.request.env['creavi_products.creavi_products'].search([]),
#         })

#     @http.route('/creavi_products/creavi_products/objects/<model("creavi_products.creavi_products"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('creavi_products.object', {
#             'object': obj
#         })
