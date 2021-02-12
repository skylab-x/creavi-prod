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

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = "sale.order"

class SaleOrderLine(models.Model):
    _name = 'sale.order.line'
    _inherit = "sale.order.line"

    width = fields.Float("Largeur (mm)")
    height = fields.Float("Hauteur (mm)")
    taux_marge = fields.Float("Marge appliquée",invisible=True)
    theorical_cost = fields.Float("Coût Théorique", readonly=True)
    selling_price_ht = fields.Float("Prix de vente HT")
    mode_impression = fields.Selection([ ('serigraphe', 'Sérigraphe'),('numerique', 'Numérique'),],'Mode d\'impression', default='numerique')

    support_id = fields.Many2one('creavi_support', string="Support")
    prix_support = fields.Float(string="Prix matière", related='support_id.price')
    width_support = fields.Float(related='support_id.width')
    height_support = fields.Float(related='support_id.height')

    projet_id = fields.Many2one('creavi_projet_fabrication', string="Projet Fabrication Creavi")

    machine_id = fields.Many2one('creavi_machine', string="Machine")
    list_machines = fields.Many2many('creavi_machine', string="Machines")
    cadence_machine = fields.Integer(related="machine_id.cadence")
    hour_cost_machine = fields.Float(related="machine_id.hour_cost")

    accessories = fields.Many2many(
        'creavi_accessoire',string='Accessoires'
    )

    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note"),
        ('line_section_with_qty', "Section avec quantité")], default=False, help="Technical field for UX purpose.")

    def init(self):
        machines = self.env['creavi_machine'].search([])
        self.list_machines = machines
        _logger.error(machines)

    def dup_line(self):
        _logger.error('dup_line')
        self.copy(default={'order_id':self.order_id.ids})

    @api.onchange('taux_marge')
    def onchange_taux_marge(self):
        if(self.taux_marge < float(self.env['ir.config_parameter'].get_param('creavi_products.marge_min'))):
            self.taux_marge = float(self.env['ir.config_parameter'].get_param('creavi_products.marge_std'))

class creaviMachine(models.Model):
    _name = "creavi_machine"
    
    name = fields.Char("Nom de machine")
    cadence = fields.Integer("Nombre d'exemplaires par heure")
    hour_cost = fields.Float("Coût Horaire")
    
class creaviConsumableInk(models.Model):
    _name = "creavi_encre"
    
    name = fields.Char("Nom de l'encre")
    price = fields.Float("Prix de l'encre au litre")
    
class creaviConsumablePaper(models.Model):
    _name = "creavi_support"
    
    name = fields.Char("Nom du support")
    price = fields.Float("Prix du support au m2")
    width = fields.Float("Largeur par unité")
    height = fields.Float("Hauteur par unité")
    
class creaviAccessory(models.Model):
    _name = "creavi_accessoire"
    
    name = fields.Char("Nom de l'accessoire")
    quantity_per_product = fields.Integer("Nombre par produit")
    tps_pose_per_product = fields.Char("Temps de pose par produit")
    tps_pose_global = fields.Char("Temps de pose global")
    
class creaviSimulation(models.Model):
    _name = "creavi_simulation"
    
    machine_id = fields.Many2one('creaviMachine.id', string="Machine Creavi")
    tps_previsionnel_machine = fields.Float("Temps Prévisionnel de fabrication")
    cout_previsionnel_machine = fields.Float("Cout Prévisionnel de la machine")
    cout_previsionnel_matieres_premieres = fields.Float("Cout Prévisionnel des matières premières")
    consommation_matieres_premieres = fields.Float("Consommation de matières premières")
    retenu = fields.Boolean("Retenu ?")
    
class creaviProjetFabrication(models.Model):
    _name = "creavi_projet_fabrication"
    
    product_id = fields.Many2one('saleOrder.id', string="Produit Creavi")
    simulation_id = fields.Many2one('creaviSimulation.id', string="Simulation Creavi")

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    marge_min = fields.Float("Marge minimum à ne pas franchir (%)")
    marge_std = fields.Float("Marge standard appliqué par défaut (%)")
    ink_m2 = fields.Float("Consommation d'encre au m2")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            marge_min = self.env['ir.config_parameter'].get_param('creavi_products.marge_min'),
            marge_std = self.env['ir.config_parameter'].get_param('creavi_products.marge_std'),
            ink_m2 = self.env['ir.config_parameter'].get_param('creavi_products.ink_m2')
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()

        self.env['ir.config_parameter'].set_param('creavi_products.marge_min', self.marge_min)
        self.env['ir.config_parameter'].set_param('creavi_products.marge_std', self.marge_std)
        self.env['ir.config_parameter'].set_param('creavi_products.ink_m2', self.ink_m2)

    @api.model
    def _check_marge_std(self):
        obj = self[0]
        if obj.marge_std < obj.marge_min:
            return False
        return True
    
    @api.model
    def _check_marge_min(self):
        obj = self[0]
        if obj.marge_min < 0:
            return False
        return True
    
    @api.model
    def _check_marge_std_not_negative(self):
        obj = self[0]
        if obj.marge_std < 0:
            return False
        return True

    @api.model
    def _check_ink_m2_not_negative(self):
        obj = self[0]
        if obj.ink_m2 < 0:
            return False
        return True
    
    _sql_constraints = [
        ('ink_m2', 'CHECK(ink_m2 >= 0)', 'La consommation d\'encre au m2 ne peut pas être négative.'),
        ('marge_std', 'CHECK(marge_std >=0)', 'La marge appliqué ne peut pas être négative'),
        ('marge_min', 'CHECK(marge_min >=0)', 'La marge minimum ne peut pas être négative'),
        ('marge_std', 'CHECK(marge_std <= marge_min', 'La marge appliqué ne peut pas être inférieur à la marge minimum')
    ]
    _constraints = [
        (_check_marge_std, "La marge appliqué ne peut pas être inférieur à la marge minimum", ['marge_std']),
        (_check_marge_min, "La marge minimum ne peut pas être négative", ['marge_min']),
        (_check_marge_std_not_negative, "La marge appliqué ne peut pas être négative", ['marge_std']),
        (_check_ink_m2_not_negative, "La consommation d'encre au m2 ne peutt pas être négative", ['ink_m2'])
    ]