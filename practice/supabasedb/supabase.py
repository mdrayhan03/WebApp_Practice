from supabase import create_client, Client
from django.conf import settings

class Supabase:
    def __init__(self) :
        url =  settings.SUPABASE_URL
        key = settings.SUPABASE_KEY

        self.base : Client = create_client(url, key)

    def create_account(self, fullname, email, password) :
        data = {
            "full_name" : fullname ,
            "email" : email ,
            "password" : password ,
            "acc_type" : 1 ,
        }

        response = self.base.table("tb_all_practice_account").insert(data).execute()
        print("Supabase create account: ", response)
        return response

    def login_account(self, email, password) :
        response = self.base.table("tb_all_practice_account").select("email").eq("email", email).eq("password", password).execute()
        print("Supabase: ", response)

        if len(response.data) == 1 :
            return True
        
        return False