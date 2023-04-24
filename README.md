# orgs

organization system

### packages

    rest_framework          (APIs)
    drf_spectacular         (swagger)
    djoser                  (user)
    knox                    (user)
    allauth                 (social login)
    modeltranslation        (model translations)
    django-hashid-field     (hash models id)
    django-extensions       (django commands)
    django-cleanup          (delete un necessary images)
    pytest                  (testing)

#### people permissions

    1. Organization admin      (super admin)
    2. Company Admin
    3. employee                (normal employee)
    4. factory admin           ( employee in company )
    5. Club admin              ( employee in company )
    6. vendors                 ( employee in company )
    7. sponsor                 ( employee in company )
    8. Guest

### Apps

1. AMS (Administration system)
2. CMS (company manage system)
3. guest app

#### some details

- when user register he can be (citizen , employee)
  -- the citizen user = has no company , can login with google
  -- the employee user = may be (company admin "or" employee in company)

- if the employee create new company he choose : # NOTE will be auto a company admin in user permission
  employee role: vendor - sponsor
  company role: internal - external

- if employee enter an existing company he choose will be:
  -- normal employee
  -- factory admin
  -- club admin
  -- vendors
  -- sponsor

- My city has more Companies
- Each Company has more Factories and Clubs
- company make products with factories
- company can make events with clubs
- companies contact with each other with companies chat
- guest and vendor can contact with each other with open chat (socket chat)
- sponsor can invest in factories by make request to company and company send this request to org admin to approve
