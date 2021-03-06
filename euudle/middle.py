from django.conf import settings
from django.http import *
from django.utils.cache import patch_vary_headers
from django.utils.log import getLogger
from datetime import *
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, get_object_or_404, HttpResponseRedirect, HttpResponse, get_list_or_404
from accounts.models import *
from stat_analysis.models import *

logger = getLogger('django.request')

class me(object):
    
    authenticated= False
    dispatch = False
    sess = ""
    redirect_to_logged = None
    
    ######################################################################
    def process_response(self, request, response):

        
        if self.authenticated == True:
            response.set_cookie('SEHS',self.sess)
            self.authenticated= False
        
        bim = request.META.get('authenticated2','')
        if bim != '':
            response.set_cookie('SEHS',bim)
            del request.META['authenticated2']
            
        if self.dispatch == True:
            bim = request.COOKIES.get('SEHS','')
            if bim is not None:
                response.set_cookie('SEHS',None)
                self.dispatch = False
      
       
        return response
    ######################################################################    
        
    def process_view( self, request, func, view_args, view_kwargs ):

        if func.__name__ == 'home' or func.__name__ == 'ajaxsearch' or func.__name__ == 'search':
            
            request.META['account'] = Sessions.objects.check_session(request.COOKIES.get('SEHS'))
            
            return None
        
        if func.__name__ == 'coursewall' or func.__name__ == 'add_coursewall' or func.__name__ == 'profile' or func.__name__ == 'review'  or func.__name__ == 'drop_course':   # and other page needed for logging in
    
            request.META['account'] = Sessions.objects.check_session(request.COOKIES.get('SEHS'))
            #return HttpResponse(str(name))
            if request.META['account'] == None:
                return HttpResponseRedirect('/')
                #return HttpResponse("You are not logged in")
            else:
                #account = Service.objects.filter(account=name)
                
                return None
        
        if func.__name__ ==  'promote':
            
            request.META['account'] = Sessions.objects.check_session(request.COOKIES.get('SEHS'))
        
        if func.__name__ == 'login':
            
            if request.method == 'POST':
                usr = request.POST.get('email','')
                pss = request.POST.get('password','') 
                t_auth, cokie = Account.objects.is_valid(usr,pss)
                if not t_auth:
		            c = {}
		            c.update(csrf(request))
		            #return render_to_response('login.html',c)
		            return HttpResponseRedirect('/')
                else:
                    self.authenticated = True
                    self.sess = cokie
                    return None
         
        if func.__name__ == 'search': 
            
            try:
                tempo_word = keyword.objects.get( word= request.GET.get('term','') )
                tempo_word.occurance += 1
                tempo_word.save()
            except:
                keyword.objects.get_or_create( word=request.GET.get('term','') )
            
            request.META['account'] = Sessions.objects.check_session(request.COOKIES.get('SEHS'))
                    
            
        
        if func.__name__ == 'logout':
            self.dispatch = True
        
        request.META['account'] = Sessions.objects.check_session(request.COOKIES.get('SEHS'))
                
        return None
