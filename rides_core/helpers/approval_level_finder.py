from apps.settings.models import ApprovalDetails, ApprovalMaster
from django.db.models import Q

class ApprovalTask():
    
    def __init__(self,section= None,current_level=1,user_instance=None,instance=None):
        self.section          = section
        self.current_level    = current_level
        self.user_instance    = user_instance
        self.instance         =  instance
    

    def next_approval_finder(self,approve_instance):

        approve_queryset = ApprovalDetails.objects.filter(Q(approval_master=approve_instance) & Q(level_of_approvals =(self.current_level)))
        print("approve_queryset",approve_queryset)
        approve_queryset = ApprovalDetails.objects.filter(Q(approval_master=approve_instance) & Q(level_of_approvals =self.current_level))
        
        if approve_instance is None or len(approve_queryset) <1:
            return None,[]
        
        approve_instance = approve_queryset.last()
        user_or_group    = approve_instance.user_or_group
        approve_res      = None

        
        match user_or_group:
            case 'User':
                approve_res = approve_instance.users.all()
            case 'Group':
                approve_res = approve_instance.groups.all()
    
        return user_or_group,approve_res
    

    def level_check(self):

        approve_instance = ApprovalMaster.objects.filter(section=self.section)
 
        if approve_instance is None or len(approve_instance) <1:
           return False,None,[]
       
        approve_instance   = approve_instance.last()
        higher_approval    = approve_instance.approval_tiers or 0 if approve_instance.approval_tiers is not None else 0

        print("self.current_level < int(higher_approval)",self.current_level < int(higher_approval))
        if self.current_level < int(higher_approval):
            user_or_group,approve_res = self.next_approval_finder(approve_instance)
            return False,user_or_group,approve_res
    
        return True,None,[]
    

    def user_access_checker(self):
        user_or_group  = self.instance.user_or_group
        print("user_or_group",user_or_group)
        print("self.user_instance",self.user_instance)
        print("self.instance.next_users.all()",self.instance.next_users.all())

        flag = False

        if user_or_group ==  'User':
            access_list  = self.instance.next_users.all()
           
            if self.user_instance in access_list:
                flag = True

        else:
            access_list  = self.instance.next_groups.all()

            users_in_group = []
            for group in access_list:
                users_in_group = group.user_set.all()
                if self.user_instance in users_in_group:
                    flag = True

        return flag