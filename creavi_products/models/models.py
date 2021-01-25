# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class creavi_products(models.Model):
#     _name = 'creavi_products.creavi_products'
#     _description = 'creavi_products.creavi_products'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

from odoo importt models, fields, api

class creaviProduct(models.Model):
    _name = "Creavi Product"
    _description = "Product Creavi"
    
    quantity = fields.Integer("Quantité")
    width = fields.Float("Largeur (cm)")
    height = fields.Float("Hauteur (cm)")
    taux_marge = fields.Float("Marge appliquée",invisible=True)
    theorical_cost = fields.Float("Coût Théorique", readonly=True)
    selling_price_ht = fields.Float("Prix de vente HT")
    projet_id = fields.Many2one('creaviProjetFabrication.id', string="Projet Fabrication Creavi")

class creaviMachine(models.Model):
    _name = "Creavi Machine"
    _description = "Machine Creavi"
    
    name = fields.Char("Nom de machine")
    type = fields.Selection([ ('serigraphe', 'Sérigraphe'),('numerique', 'Numérique'),],'Type de machine', default='numerique')
    cadence = fields.Integer("Nombre d'exemplaires par heure")
    hour_cost = fields.Float("Coût Horaire")
    
class creaviConsumableInk(models.Model):
    _name = "Creavi Consommable - Encres"
    _description = "Consommable Encres Creavi"
    
    name = fields.Char("Nom de l'encre")
    price = fields.Float("Prix de l'encre au litre")
    
class creaviConsumablePaper(models.Model):
    _name = "Creavi Consommable - Papier"
    _description = "Consommable Papiers Creavi"
    
    name = fields.Char("Nom du papier")
    price = fields.Float("Prix du papier au m2")
    
class creaviAccessory(models.Model):
    _name = "Creavi Accessoire"
    _description = "Accessoire Creavi"
    
    name = fields.Char("Nom de l'accessoire")
    quantity_per_product = fields.Integer("Nombre par produit")
    tps_pose_per_product = fields.Char("Temps de pose par produit")
    tps_pose_global = fields.Char("Temps de pose global")
    
class creaviSimulation(models.Model):
    _name = "Creavi Simulation"
    _description = "Simulation Creavi"
    
    machine_id = fields.Many2one('creaviMachine.id', string="Machine Creavi")
    tps_previsionnel_machine = fields.Float("Temps Prévisionnel de fabrication")
    cout_previsionnel_machine = fields.Float("Cout Prévisionnel de la machine")
    cout_previsionnel_matieres_premieres = fields.Float("Cout Prévisionnel des matières premières")
    consommation_matieres_premieres = fields.Float("Consommation de matières premières")
    retenu = fields.Boolean("Retenu ?")
    
class creaviProjetFabrication(models.Model):
    _name = "Creavi Projet Fabrication"
    _description = "Projet Fabrication Creavi"
    
    product_id = fields.Many2one('creaviProduct.id', string="Produit Creavi")
    simulation_id = fields.Many2one('creaviSimulation.id', string="Simulation Creavi")