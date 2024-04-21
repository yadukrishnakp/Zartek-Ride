from django.db.models import Q, Sum
from apps.clientmanagement.models import EnquiryDetails, EnquiryMaster
from apps.sales.models import OrderItem, SalesOrder
from rides_core.helpers.helper import get_object_or_none

"""Enquiry section"""
class EnquiryMasterAmount():
    
    def __init__(self, enquirymaster=None):
        self.enquirymaster                  = enquirymaster

    def total_amounts(self):
        enquirymaster = get_object_or_none(EnquiryMaster,pk=self.enquirymaster.pk)

        total_amounts = EnquiryDetails.objects.filter(Q(enquiry=enquirymaster)).aggregate(discount_amount=Sum('discount_amount'),gross_amount=Sum('gross_amount'),unit_cost_foc=Sum('unit_cost_foc'),unit_cost_lc=Sum('unit_cost_lc'),overhead_amount=Sum('overhead_amount'),net_cost=Sum('net_cost'),other_charges=Sum('other_charges'))
        
        enquirymaster.total_discount        = total_amounts.get('discount_amount',0)
        enquirymaster.total_gross           = total_amounts.get('gross_amount',0)
        enquirymaster.total_unit_cost_foc   = total_amounts.get('unit_cost_foc',0)
        enquirymaster.total_unit_cost_lc    = total_amounts.get('unit_cost_lc',0)
        enquirymaster.total_overhead_amount = total_amounts.get('overhead_amount',0)
        enquirymaster.total_net_cost        = total_amounts.get('net_cost',0)
        enquirymaster.total_other_charges   = total_amounts.get('other_charges',0)
        enquirymaster.save()
        
        return 
    

"""Sales Order"""
class SaleOrderAmount():
    def __init__(self, amount=None,discount=None,saleorder=None):
        self.amount   = amount
        self.discount = discount
        self.saleorder = saleorder

    def individual_discounts(self):
        final_amount,discount_amount=None,None

        if self.amount not in [None,''] and self.discount not in ['',None]:
            discount_amount   = (float(self.amount)*float(self.discount))/100
            final_amount      = float(self.amount) -discount_amount
        return final_amount,discount_amount

    def total_finder(self):
        instance                = get_object_or_none(SalesOrder,pk=self.saleorder.id)

        total_amounts           = OrderItem.objects.filter(Q(order=instance)).aggregate(final_amount=Sum('final_amount'))
        instance.final_amount   = total_amounts.get('final_amount')
        instance.save()
        return 
