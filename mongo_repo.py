import pymongo

from pymongo import MongoClient
from User import User


class mongoRepo:
    download_counter = 0

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.users = client.mU.vws_Users
        self.docs = client.mU.mU_documents

    def user_factory(self,user_cursor):
        """Creates user object from mongo cursor"""
        u = User()
        u.id = user_cursor.get("_id")
        u.download_list = user_cursor.get("downloadList")
        u.realms = user_cursor.get("realms")
        u.school_classes = user_cursor.get("schoolclasses")
        u.subjects_list = user_cursor.get("subjects")
        u.city = user_cursor.get("city")
        u.country = user_cursor.get("country")
        u.area_code = user_cursor.get("areaCode")
        u.gender = user_cursor.get("gender")
        u.schools = user_cursor.get("schools")
        u.school_type_list = []
        u.downloads = []

        # create a clean list of school types
        for school in u.schools:
            try:
                u.school_type_list.append(school["type"].encode('utf-8'))
            except (TypeError, AttributeError) as err:
                print("")

        try:
            u.school_type = "|".join(u.school_type_list)
        except (TypeError, AttributeError) as err:
            u.school_type = ""

        try:
            # create a list of downloaded ids
            for doc in u.download_list:
                u.downloads.append(doc["doc_id"])
        except TypeError as err:
            print("")

        try:
            temp_sub = []
            for subject in u.subjects_list:
                temp_sub.append(subject.encode('utf-8'))

            u.subjects = "|".join(temp_sub)

            tmp_realm = []
            for r in u.realms:
                tmp_realm.append(r)

            u.realm = " | ".join(tmp_realm)

            try:
                tmp_classes = []
                for c in u.school_classes:
                    tmp_classes.append(c)

                u.classes = " | ".join(tmp_classes)
            except (TypeError) as err:
                u.classes = ''

        except (TypeError, AttributeError) as err:
            print("")

        return u
    def get_documents(self):

       client = MongoClient('mongo', 27017)
       docs = client.mU.mU_documents

       print('fetching documents')
       result = docs.find({}).limit(5)

       print('done')
       for r in result:
            print(r.get("_id"))


    def get_premium_users(self):
        """Fetchs a list of premium users from mongodb """
        client = MongoClient('mongo', 27017)
        self.users = client.mU.vws_Users
        result = self.users.find({'type': 2}).limit(10)
        user_list = []

        for r in result:
            user = self.user_factory(r)

            print("User id: {0} processing ".format(user.id))
            print("Download count is : {0}".format(len(user.downloads)))
            print("\t")
            print("===============================")
            for d in user.downloads:

                try:
                    print(d)
                except AttributeError:
                    print("")

            self.download_counter += len(user.downloads)
            print("===============================")
            user_list.append(user)

        return user_list
