-- user groups/roles --
INSERT INTO auth_group(name) VALUES ('Drivers');
INSERT INTO auth_group(name) VALUES ('Dispatchers');
INSERT INTO auth_group(name) VALUES ('Managers');
INSERT INTO auth_group(name) VALUES ('Clients');

-- give groups permissions --
    -- Dispatchers --
        -- User model --
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='change_user';
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='view_user';
        -- UserProfile model --
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='change_userprofile';
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='view_userprofile';
        -- Load model --
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='add_load';
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='change_load';
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='delete_load';
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='view_load';
        -- Driver model --
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='add_driver';
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='change_driver';
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='delete_driver';
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='view_driver';
        -- Truck model --
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='add_truck';
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='change_truck';
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='delete_truck';
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='view_truck';
        -- Trailer model --
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='add_trailer';
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='change_trailer';
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='delete_trailer';
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='view_trailer';
        -- Route model --
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='add_route';
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='change_route';
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='delete_route';
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='view_route';
        -- Company model --
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='view_company';
        -- Location model --
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='add_location';
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='change_location';
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='view_location';
        -- RouteStop model --
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='add_routestop';
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='change_routestop';
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='delete_routestop';
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='view_routestop';
        -- Dispatcher model --
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='change_dispatcher';
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='view_dispatcher';

    -- Drivers --
        -- User model --
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Drivers'),id FROM auth_permission WHERE codename='change_user';
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Drivers'),id FROM auth_permission WHERE codename='view_user';
        -- UserProfile model --
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Drivers'),id FROM auth_permission WHERE codename='change_userprofile';
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Drivers'),id FROM auth_permission WHERE codename='view_userprofile';
        -- Load model --
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Drivers'),id FROM auth_permission WHERE codename='view_load';
        -- Driver model --
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Drivers'),id FROM auth_permission WHERE codename='view_driver';
        -- Route model --
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Drivers'),id FROM auth_permission WHERE codename='view_route';
        -- RouteStop model --
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='add_routestop';
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='change_routestop';
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='delete_routestop';
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'),id FROM auth_permission WHERE codename='view_routestop';

    -- Managers --
        INSERT INTO auth_group_permissions(group_id,permission_id) SELECT (SELECT id FROM auth_group WHERE name='Managers'),id FROM auth_permission WHERE codename LIKE '%';
    
-- crm_companyindustry; -- 
INSERT INTO crm_companyindustry(name) VALUES ('Transport');
INSERT INTO crm_companyindustry(name) VALUES ('Services');
INSERT INTO crm_companyindustry(name) VALUES ('Food');
INSERT INTO crm_companyindustry(name) VALUES ('Consulting');

-- crm_company KMS Express  --
INSERT INTO crm_company(name,phone_number,dot_number,mc_number,website,email) VALUES ('KMS Express','+12124567890',1234567,1234567,'http://kmsexpressinc.com','kms@kms.com');
    -- KMS Express industries --
    INSERT INTO crm_company_industries(company_id,companyindustry_id) SELECT (SELECT id FROM crm_company WHERE name='KMS Express'),id FROM crm_companyindustry WHERE name='Transport';
    INSERT INTO crm_company_industries(company_id,companyindustry_id) SELECT (SELECT id FROM crm_company WHERE name='KMS Express'),id FROM crm_companyindustry WHERE name='Services';

-- user 'dd' with password 28112002%$dusko --
INSERT INTO auth_user(password,last_login,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined) VALUES ('pbkdf2_sha256$870000$KnlJWAR0SXgz01OTRyyKHH$YQA1DaiE2QLOog9PRdMmB43qQbkZRwmiajXBYeV46sA=',NULL,'f','d','d','d','dd@dd.com','f','t',NOW());
INSERT INTO core_userprofile(is_email_verified,phone_number,company_id,user_id)  SELECT 't','+12124567890',(SELECT id FROM crm_company WHERE name='KMS Express'),id FROM auth_user WHERE email='dd@dd.com';
    -- make 'dd' a dispatcher
    INSERT INTO user_management_dispatcher(userprofile_ptr_id) SELECT id FROM auth_user WHERE email='dd@dd.com';
    INSERT INTO auth_user_groups(group_id,user_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'), id FROM auth_user WHERE email='dd@dd.com';
    
    -- make 'dd' a driver for himself
    INSERT INTO user_management_driver(userprofile_ptr_id,assigned_dispatcher_id,is_hazmat_endorsed,is_tanker_endorsed,pay_rate,status,payment_type) SELECT id,id,'t','t',420.69,'STANDBY','$MILE' FROM auth_user WHERE email='dd@dd.com';
    INSERT INTO auth_user_groups(group_id,user_id) SELECT (SELECT id FROM auth_group WHERE name='Drivers'), id FROM auth_user WHERE email='dd@dd.com';

-- user 'stefy' with password 28112002%$dusko --
INSERT INTO auth_user(password,last_login,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined) VALUES ('pbkdf2_sha256$870000$w41U5UoVNNFYLGgSwOIuWd$JRs7kptUr5prNpJDqaCQpseAIlFKaL5vHz/FFwWMoN4=',NULL,'f','stefy','Stefan','Fast','stefan@stefan.com','f','t',NOW());
INSERT INTO core_userprofile(is_email_verified,phone_number,company_id,user_id)  SELECT 't','+12124567890',(SELECT id FROM crm_company WHERE name='KMS Express'),id FROM auth_user WHERE email='stefan@stefan.com';
    -- make 'stefy' a dispatcher
    INSERT INTO user_management_dispatcher(userprofile_ptr_id) SELECT id FROM auth_user WHERE email='stefan@stefan.com';
    INSERT INTO auth_user_groups(group_id,user_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'), id FROM auth_user WHERE email='stefan@stefan.com';

-- user 'trify' with password 28112002%$dusko --
INSERT INTO auth_user(password,last_login,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined) VALUES ('pbkdf2_sha256$870000$w41U5UoVNNFYLGgSwOIuWd$JRs7kptUr5prNpJDqaCQpseAIlFKaL5vHz/FFwWMoN4=',NULL,'f','trify','Trifun','Smart','trifun@trifun.com','f','t',NOW());
INSERT INTO core_userprofile(is_email_verified,phone_number,company_id,user_id)  SELECT 't','+12124567890',(SELECT id FROM crm_company WHERE name='KMS Express'),id FROM auth_user WHERE email='trifun@trifun.com';
    -- make 'trify' a driver for 'stefy'
    INSERT INTO user_management_driver(userprofile_ptr_id,assigned_dispatcher_id,is_hazmat_endorsed,is_tanker_endorsed,pay_rate,status,payment_type) SELECT (SELECT id FROM auth_user WHERE email='trifun@trifun.com'),id,'t','t',420.69,'STANDBY','$MILE' FROM auth_user WHERE email='stefan@stefan.com';
    INSERT INTO auth_user_groups(group_id,user_id) SELECT (SELECT id FROM auth_group WHERE name='Drivers'), id FROM auth_user WHERE email='trifun@trifun.com';

-- user 'richard' with password 28112002%$dusko --
INSERT INTO auth_user(password,last_login,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined) VALUES ('pbkdf2_sha256$870000$w41U5UoVNNFYLGgSwOIuWd$JRs7kptUr5prNpJDqaCQpseAIlFKaL5vHz/FFwWMoN4=',NULL,'f','richard','Richard','slow','richard@richard.com','f','t',NOW());
INSERT INTO core_userprofile(is_email_verified,phone_number,company_id,user_id)  SELECT 't','+12124567890',(SELECT id FROM crm_company WHERE name='KMS Express'),id FROM auth_user WHERE email='richard@richard.com';
    -- make 'richard' a driver for 'stefy'
    INSERT INTO user_management_driver(userprofile_ptr_id,assigned_dispatcher_id,is_hazmat_endorsed,is_tanker_endorsed,pay_rate,status,payment_type) SELECT (SELECT id FROM auth_user WHERE email='richard@richard.com'),id,'t','t',420.69,'STANDBY','$MILE' FROM auth_user WHERE email='stefan@stefan.com';
    INSERT INTO auth_user_groups(group_id,user_id) SELECT (SELECT id FROM auth_group WHERE name='Drivers'), id FROM auth_user WHERE email='richard@richard.com';

-- user 'WILLIAM' with password 28112002%$dusko --
INSERT INTO auth_user(password,last_login,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined) VALUES ('pbkdf2_sha256$870000$w41U5UoVNNFYLGgSwOIuWd$JRs7kptUr5prNpJDqaCQpseAIlFKaL5vHz/FFwWMoN4=',NULL,'f','WILLIAM','WILLIAM','LIPPOLD','william@william.com','f','t',NOW());
INSERT INTO core_userprofile(is_email_verified,phone_number,company_id,user_id)  SELECT 't',NULL,(SELECT id FROM crm_company WHERE name='KMS Express'),id FROM auth_user WHERE email='william@william.com';
    -- make 'WILLIAM' a driver for 'stefy'
    INSERT INTO user_management_driver(userprofile_ptr_id,assigned_dispatcher_id,is_hazmat_endorsed,is_tanker_endorsed,pay_rate,status,payment_type) SELECT (SELECT id FROM auth_user WHERE email='william@william.com'),id,'t','t',420.69,'STANDBY','$MILE' FROM auth_user WHERE email='stefan@stefan.com';
    INSERT INTO auth_user_groups(group_id,user_id) SELECT (SELECT id FROM auth_group WHERE name='Drivers'), id FROM auth_user WHERE email='william@william.com';

-- trailers for KMS Express --
    INSERT INTO equipment_management_trailer(created_at , updated_at , is_leased , lease_rate , vin , status , type, is_active, weigth_lbs, length_ft, assigned_driver_id, company_id) SELECT NOW(),NOW(),'f',0.0,'R66572','STANDBY','VAN','t',NULL,NULL,(SELECT id FROM auth_user WHERE email='trifun@trifun.com'),id FROM crm_company WHERE name='KMS Express';
    INSERT INTO equipment_management_trailer(created_at , updated_at , is_leased , lease_rate , vin , status , type, is_active, weigth_lbs, length_ft, assigned_driver_id, company_id) SELECT NOW(),NOW(),'t',1200.00,'RF5139','STANDBY','REFEER','t',NULL,18,(SELECT id FROM auth_user WHERE email='richard@richard.com'),id FROM crm_company WHERE name='KMS Express';
    INSERT INTO equipment_management_trailer(created_at , updated_at , is_leased , lease_rate , vin , status , type, is_active, weigth_lbs, length_ft, assigned_driver_id, company_id) SELECT NOW(),NOW(),'t',600.00,'DR1119','STANDBY','DRYVAN','t',2500,27,NULL,id FROM crm_company WHERE name='KMS Express';
    INSERT INTO equipment_management_trailer(created_at , updated_at , is_leased , lease_rate , vin , status , type, is_active, weigth_lbs, length_ft, assigned_driver_id, company_id) SELECT NOW(),NOW(),'f',0.0,'FF123','STANDBY','VAN','t',3700,22,NULL,id FROM crm_company WHERE name='KMS Express';
    INSERT INTO equipment_management_trailer(created_at , updated_at , is_leased , lease_rate , vin , status , type, is_active, weigth_lbs, length_ft, assigned_driver_id, company_id) SELECT NOW(),NOW(),'f',0.0,'IILS231','STANDBY','DRYVAN','t',600,12,NULL,id FROM crm_company WHERE name='KMS Express';
    INSERT INTO equipment_management_trailer(created_at , updated_at , is_leased , lease_rate , vin , status , type, is_active, weigth_lbs, length_ft, assigned_driver_id, company_id) SELECT NOW(),NOW(),'f',0.0,'OODLL13','STANDBY','REFEER','t',2200,34,NULL,id FROM crm_company WHERE name='KMS Express';
    
-- trucks for KMS Express -- 
    INSERT INTO equipment_management_truck(created_at , updated_at , is_leased , lease_rate , vin , status, is_active, weigth_lbs, length_ft, assigned_driver_id, company_id) SELECT NOW(),NOW(),'f',0.0,'R88139','STANDBY','t',2600,13,(SELECT id FROM auth_user WHERE email='trifun@trifun.com'),id FROM crm_company WHERE name='KMS Express';
    INSERT INTO equipment_management_truck(created_at , updated_at , is_leased , lease_rate , vin , status, is_active, weigth_lbs, length_ft, assigned_driver_id, company_id) SELECT NOW(),NOW(),'t',666.49,'SSS123','STANDBY','t',NULL,26,NULL,id FROM crm_company WHERE name='KMS Express';
    INSERT INTO equipment_management_truck(created_at , updated_at , is_leased , lease_rate , vin , status, is_active, weigth_lbs, length_ft, assigned_driver_id, company_id) SELECT NOW(),NOW(),'f',0.0,'1FUJHHDR0NLNB5627','STANDBY','t',1600,NULL,NULL,id FROM crm_company WHERE name='KMS Express';
    INSERT INTO equipment_management_truck(created_at , updated_at , is_leased , lease_rate , vin , status, is_active, weigth_lbs, length_ft, assigned_driver_id, company_id) SELECT NOW(),NOW(),'t',420.99,'DSS312335','STANDBY','t',1600,NULL,NULL,id FROM crm_company WHERE name='KMS Express';
    INSERT INTO equipment_management_truck(created_at , updated_at , is_leased , lease_rate , vin , status, is_active, weigth_lbs, length_ft, assigned_driver_id, company_id) SELECT NOW(),NOW(),'f',0.0,'33NFHD92','STANDBY','t',4200,23,NULL,id FROM crm_company WHERE name='KMS Express';





-- crm_company for CRM testing  --
INSERT INTO crm_company(name,website,phone_number) VALUES ('1440 Foods','https://1440foods.com',NULL);
INSERT INTO crm_company(name,website,phone_number) VALUES ('Hampton Farms','https://hamptonfarms.com','+18003132748');
INSERT INTO crm_company(name,website,phone_number) VALUES ('Harbor Foodservice','https://harborfoodservice.com','+14252511376');
INSERT INTO crm_company(name,website,phone_number) VALUES ('85C Bakery Cafe','https://85cbakerycafe.com','+17144591685');
INSERT INTO crm_company(name,website,phone_number) VALUES ('ABC Fine Wine & Spirits','https://abcfws.com','+18664506622');
-- company industries --
    -- 1440 Foods --
    INSERT INTO crm_company_industries(company_id,companyindustry_id) SELECT (SELECT id FROM crm_company WHERE name='1440 Foods'),id FROM crm_companyindustry WHERE name='Services';
    INSERT INTO crm_company_industries(company_id,companyindustry_id) SELECT (SELECT id FROM crm_company WHERE name='1440 Foods'),id FROM crm_companyindustry WHERE name='Food';
    -- Hampton Farms --
    INSERT INTO crm_company_industries(company_id,companyindustry_id) SELECT (SELECT id FROM crm_company WHERE name='Hampton Farms'),id FROM crm_companyindustry WHERE name='Food';
    -- Harbor Foodservice --
    INSERT INTO crm_company_industries(company_id,companyindustry_id) SELECT (SELECT id FROM crm_company WHERE name='Harbor Foodservice'),id FROM crm_companyindustry WHERE name='Food';
    INSERT INTO crm_company_industries(company_id,companyindustry_id) SELECT (SELECT id FROM crm_company WHERE name='Harbor Foodservice'),id FROM crm_companyindustry WHERE name='Services';
    INSERT INTO crm_company_industries(company_id,companyindustry_id) SELECT (SELECT id FROM crm_company WHERE name='Harbor Foodservice'),id FROM crm_companyindustry WHERE name='Transport';
    INSERT INTO crm_company_industries(company_id,companyindustry_id) SELECT (SELECT id FROM crm_company WHERE name='Harbor Foodservice'),id FROM crm_companyindustry WHERE name='Consulting';
    -- 85C Bakery Cafe --
    INSERT INTO crm_company_industries(company_id,companyindustry_id) SELECT (SELECT id FROM crm_company WHERE name='85C Bakery Cafe'),id FROM crm_companyindustry WHERE name='Food';
    INSERT INTO crm_company_industries(company_id,companyindustry_id) SELECT (SELECT id FROM crm_company WHERE name='85C Bakery Cafe'),id FROM crm_companyindustry WHERE name='Services';
    -- ABC Fine Wine & Spirits --
    INSERT INTO crm_company_industries(company_id,companyindustry_id) SELECT (SELECT id FROM crm_company WHERE name='ABC Fine Wine & Spirits'),id FROM crm_companyindustry WHERE name='Food';

-- ABC Fine Wine & Spirits --
-- debbiel@abcfws.com with password 28112002%$dusko is a dispatcher -- 
INSERT INTO auth_user(password,last_login,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined) VALUES ('pbkdf2_sha256$870000$w41U5UoVNNFYLGgSwOIuWd$JRs7kptUr5prNpJDqaCQpseAIlFKaL5vHz/FFwWMoN4=',NULL,'f','DebbieLeatherland','Debbie','Leatherland','debbiel@abcfws.com','f','t',NOW());
INSERT INTO core_userprofile(is_email_verified,phone_number,company_id,user_id)  SELECT 't',NULL,(SELECT id from crm_company WHERE name='ABC Fine Wine & Spirits'),id FROM auth_user WHERE email='debbiel@abcfws.com';
    -- make 'debbiel@abcfws.com' a dispatcher
    INSERT INTO user_management_dispatcher(userprofile_ptr_id) SELECT id FROM auth_user WHERE email='debbiel@abcfws.com';
    INSERT INTO auth_user_groups(group_id,user_id) SELECT (SELECT id FROM auth_group WHERE name='Dispatchers'), id FROM auth_user WHERE email='debbiel@abcfws.com';

-- kris@kris.com is a Driver for debbiel@abcfws.com -- 
INSERT INTO auth_user(password,last_login,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined) VALUES ('pbkdf2_sha256$870000$w41U5UoVNNFYLGgSwOIuWd$JRs7kptUr5prNpJDqaCQpseAIlFKaL5vHz/FFwWMoN4=',NULL,'f','KrisBecker','Kris','Becker','kris@kris.com','f','t',NOW());
INSERT INTO core_userprofile(is_email_verified,phone_number,company_id,user_id)  SELECT 't',NULL,(SELECT id from crm_company WHERE name='ABC Fine Wine & Spirits'),id FROM auth_user WHERE email='kris@kris.com';
    -- make 'kris@kris.com' a driver for 'debbiel@abcfws.com'
    INSERT INTO user_management_driver(userprofile_ptr_id,assigned_dispatcher_id,is_hazmat_endorsed,is_tanker_endorsed,pay_rate,status,payment_type) SELECT (SELECT id FROM auth_user WHERE email='kris@kris.com'),id,'t','t',420.69,'STANDBY','$MILE' FROM auth_user WHERE email='debbiel@abcfws.com';
    INSERT INTO auth_user_groups(group_id,user_id) SELECT (SELECT id FROM auth_group WHERE name='Drivers'), id FROM auth_user WHERE email='kris@kris.com';

-- dave@dave.com is a Driver for debbiel@abcfws.com -- 
INSERT INTO auth_user(password,last_login,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined) VALUES ('pbkdf2_sha256$870000$w41U5UoVNNFYLGgSwOIuWd$JRs7kptUr5prNpJDqaCQpseAIlFKaL5vHz/FFwWMoN4=',NULL,'f','DaveLarue','Dave','Larue','dave@dave.com','f','t',NOW());
INSERT INTO core_userprofile(is_email_verified,phone_number,company_id,user_id) SELECT 't',NULL,(SELECT id from crm_company WHERE name='ABC Fine Wine & Spirits'),id FROM auth_user WHERE email='dave@dave.com';
    -- make 'dave@dave.com' a driver for 'debbiel@abcfws.com'
    INSERT INTO user_management_driver(userprofile_ptr_id,assigned_dispatcher_id,is_hazmat_endorsed,is_tanker_endorsed,pay_rate,status,payment_type) SELECT (SELECT id FROM auth_user WHERE email='dave@dave.com'),id,'t','t',420.69,'STANDBY','$MILE' FROM auth_user WHERE email='debbiel@abcfws.com';
    INSERT INTO auth_user_groups(group_id,user_id) SELECT (SELECT id FROM auth_group WHERE name='Drivers'), id FROM auth_user WHERE email='dave@dave.com';

-- 85C Bakery Cafe --
INSERT INTO auth_user(password,last_login,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined) VALUES ('pbkdf2_sha256$870000$w41U5UoVNNFYLGgSwOIuWd$JRs7kptUr5prNpJDqaCQpseAIlFKaL5vHz/FFwWMoN4=',NULL,'f','NeilMoody','Neil','Moody','neil@neil.com','f','t',NOW());
INSERT INTO core_userprofile(is_email_verified,phone_number,company_id,user_id)  SELECT 't',NULL,(SELECT id from crm_company WHERE name='85C Bakery Cafe'),id FROM auth_user WHERE email='neil@neil.com';
INSERT INTO auth_user(password,last_login,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined) VALUES ('pbkdf2_sha256$870000$w41U5UoVNNFYLGgSwOIuWd$JRs7kptUr5prNpJDqaCQpseAIlFKaL5vHz/FFwWMoN4=',NULL,'f','Jovanni','Jovanni','Alvarado','jovanni@jovanni.com','f','t',NOW());
INSERT INTO core_userprofile(is_email_verified,phone_number,company_id,user_id) SELECT 't',NULL,(SELECT id from crm_company WHERE name='85C Bakery Cafe'),id FROM auth_user WHERE email='jovanni@jovanni.com';
INSERT INTO auth_user(password,last_login,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined) VALUES ('pbkdf2_sha256$870000$w41U5UoVNNFYLGgSwOIuWd$JRs7kptUr5prNpJDqaCQpseAIlFKaL5vHz/FFwWMoN4=',NULL,'f','kim','kim','do','kim@kim.com','f','t',NOW());
INSERT INTO core_userprofile(is_email_verified,phone_number,company_id,user_id)  SELECT 't',NULL,(SELECT id from crm_company WHERE name='85C Bakery Cafe'),id FROM auth_user WHERE email='kim@kim.com';


-- Harbor Foodservice --
INSERT INTO auth_user(password,last_login,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined) VALUES ('pbkdf2_sha256$870000$w41U5UoVNNFYLGgSwOIuWd$JRs7kptUr5prNpJDqaCQpseAIlFKaL5vHz/FFwWMoN4=',NULL,'f','mark','mark','Seven','mark@mark.com','f','t',NOW());
INSERT INTO core_userprofile(is_email_verified,phone_number,company_id,user_id)  SELECT 't',NULL,(SELECT id from crm_company WHERE name='Harbor Foodservice'),id FROM auth_user WHERE email='mark@mark.com';
INSERT INTO auth_user(password,last_login,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined) VALUES ('pbkdf2_sha256$870000$w41U5UoVNNFYLGgSwOIuWd$JRs7kptUr5prNpJDqaCQpseAIlFKaL5vHz/FFwWMoN4=',NULL,'f','stoyan','Stoyan','Eight','stoyan@stoyan.com','f','t',NOW());
INSERT INTO core_userprofile(is_email_verified,phone_number,company_id,user_id)  SELECT 't',NULL,(SELECT id from crm_company WHERE name='Harbor Foodservice'),id FROM auth_user WHERE email='stoyan@stoyan.com';
INSERT INTO auth_user(password,last_login,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined) VALUES ('pbkdf2_sha256$870000$w41U5UoVNNFYLGgSwOIuWd$JRs7kptUr5prNpJDqaCQpseAIlFKaL5vHz/FFwWMoN4=',NULL,'f','kosta','Kosta','Nine','kosta@kosta.com','f','t',NOW());
INSERT INTO core_userprofile(is_email_verified,phone_number,company_id,user_id)  SELECT 't',NULL,(SELECT id from crm_company WHERE name='Harbor Foodservice'),id FROM auth_user WHERE email='kosta@kosta.com';

-- Hampton Farms --
INSERT INTO auth_user(password,last_login,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined) VALUES ('pbkdf2_sha256$870000$w41U5UoVNNFYLGgSwOIuWd$JRs7kptUr5prNpJDqaCQpseAIlFKaL5vHz/FFwWMoN4=',NULL,'f','lily','lily','Ten','lily@lily.com','f','t',NOW());
INSERT INTO core_userprofile(is_email_verified,phone_number,company_id,user_id)  SELECT 't',NULL,(SELECT id from crm_company WHERE name='Hampton Farms'),id FROM auth_user WHERE email='lily@lily.com';
INSERT INTO auth_user(password,last_login,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined) VALUES ('pbkdf2_sha256$870000$w41U5UoVNNFYLGgSwOIuWd$JRs7kptUr5prNpJDqaCQpseAIlFKaL5vHz/FFwWMoN4=',NULL,'f','soa','Soa','Eleven','soa@soa.com','f','t',NOW());
INSERT INTO core_userprofile(is_email_verified,phone_number,company_id,user_id)  SELECT 't',NULL,(SELECT id from crm_company WHERE name='Hampton Farms'),id FROM auth_user WHERE email='soa@soa.com';

-- 1440 Foods --
INSERT INTO auth_user(password,last_login,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined) VALUES ('pbkdf2_sha256$870000$w41U5UoVNNFYLGgSwOIuWd$JRs7kptUr5prNpJDqaCQpseAIlFKaL5vHz/FFwWMoN4=',NULL,'f','mia','Mia','Twelve','mia@mia.com','f','t',NOW());
INSERT INTO core_userprofile(is_email_verified,phone_number,company_id,user_id)  SELECT 't',NULL,(SELECT id from crm_company WHERE name='1440 Foods'),id FROM auth_user WHERE email='mia@mia.com';





-- -- Loads ---
--     -- Load from Chicago to Milwaukee using 'distance_miles' as the unique field for the selection. --
--     -- no assigned driver --
--     INSERT INTO dispatch_load(id,created_at,updated_at,is_hazmat,revenue,weigth_lbs,status,route_id) SELECT gen_random_uuid(),NOW(),NOW(),'f',420,1999,'WAITING',id FROM dispatch_route WHERE distance_miles = 69;
--     INSERT INTO dispatch_load(id,created_at,updated_at,is_hazmat,revenue,weigth_lbs,status,route_id) SELECT gen_random_uuid(),NOW(),NOW(),'t',3250,750,'ON ROAD',id FROM dispatch_route WHERE distance_miles = 69;
--     INSERT INTO dispatch_load(id,created_at,updated_at,is_hazmat,revenue,weigth_lbs,status,route_id) SELECT gen_random_uuid(),NOW(),NOW(),'t',667,3500,'ON ROAD',id FROM dispatch_route WHERE distance_miles = 69;
--     INSERT INTO dispatch_load(id,created_at,updated_at,is_hazmat,revenue,weigth_lbs,status,route_id) SELECT gen_random_uuid(),NOW(),NOW(),'t',1234,999,'DELIVERED',id FROM dispatch_route WHERE distance_miles = 69;

--     -- Load from Chicago to Milwaukee using 'distance_miles' as the unique field for the selection.--
--     -- dd is the driver  (who is also a dispatcher for himself) --
--     INSERT INTO dispatch_load(id,created_at,updated_at,is_hazmat,revenue,weigth_lbs,status,driver_id,route_id) SELECT gen_random_uuid(),NOW(),NOW(),'t',567,891,'WAITING',(SELECT  id FROM auth_user WHERE email='lopd4321@gmail.com'), id FROM dispatch_route WHERE distance_miles = 69;
--     INSERT INTO dispatch_load(id,created_at,updated_at,is_hazmat,revenue,weigth_lbs,status,driver_id,route_id) SELECT gen_random_uuid(),NOW(),NOW(),'t',15,90,'ON ROAD',(SELECT  id FROM auth_user WHERE email='lopd4321@gmail.com'), id FROM dispatch_route WHERE distance_miles = 69;
--     INSERT INTO dispatch_load(id,created_at,updated_at,is_hazmat,revenue,weigth_lbs,status,driver_id,route_id) SELECT gen_random_uuid(),NOW(),NOW(),'t',1,0,'DELIVERED',(SELECT  id FROM auth_user WHERE email='lopd4321@gmail.com'), id FROM dispatch_route WHERE distance_miles = 69;
    
--     -- Load from Chicago to Milwaukee using 'distance_miles' as the unique field for the selection.--
--     -- trify is the driver for stefy --
--     INSERT INTO dispatch_load(id,created_at,updated_at,is_hazmat,revenue,weigth_lbs,status,driver_id,route_id) SELECT gen_random_uuid(),NOW(),NOW(),'t',15,90,'ON ROAD',(SELECT  id FROM auth_user WHERE email='trifun@trifun.com'), id FROM dispatch_route WHERE distance_miles = 69;
--     INSERT INTO dispatch_load(id,created_at,updated_at,is_hazmat,revenue,weigth_lbs,status,driver_id,route_id) SELECT gen_random_uuid(),NOW(),NOW(),'t',1,0,'DELIVERED',(SELECT  id FROM auth_user WHERE email='trifun@trifun.com'), id FROM dispatch_route WHERE distance_miles = 69;
--     -- same except that the pickup_datetime is set to NOW() --
--     INSERT INTO dispatch_load(id,created_at,updated_at,is_hazmat,revenue,weigth_lbs,status,pickup_datetime,driver_id,route_id) SELECT gen_random_uuid(),NOW(),NOW(),'t',1,0,'DELIVERED',NOW(),(SELECT  id FROM auth_user WHERE email='trifun@trifun.com'), id FROM dispatch_route WHERE distance_miles = 69;

--     -- Load from Rockford to Burlington using 'distance_miles' as the unique field for the selection.--
--     -- trify is the driver for stefy --
--     INSERT INTO dispatch_load(id,created_at,updated_at,is_hazmat,revenue,weigth_lbs,status,driver_id,route_id) SELECT gen_random_uuid(),NOW(),NOW(),'t',15,90,'ON ROAD',(SELECT  id FROM auth_user WHERE email='trifun@trifun.com'), id FROM dispatch_route WHERE distance_miles = 70;
--     INSERT INTO dispatch_load(id,created_at,updated_at,is_hazmat,revenue,weigth_lbs,status,driver_id,route_id) SELECT gen_random_uuid(),NOW(),NOW(),'t',1,0,'DELIVERED',(SELECT  id FROM auth_user WHERE email='trifun@trifun.com'), id FROM dispatch_route WHERE distance_miles = 70;
--     -- same except that the pickup_datetime is set to NOW() --
--     INSERT INTO dispatch_load(id,created_at,updated_at,is_hazmat,revenue,weigth_lbs,status,pickup_datetime,driver_id,route_id) SELECT gen_random_uuid(),NOW(),NOW(),'t',1,0,'DELIVERED',NOW(),(SELECT  id FROM auth_user WHERE email='trifun@trifun.com'), id FROM dispatch_route WHERE distance_miles = 70;

--     -- Load from "Chicago -> Milwaukee" -> "Rockford -> Burlington" using 'distance_miles' as the unique field for the selection.--
--     -- trify is the driver for stefy --
--     INSERT INTO dispatch_load(id,created_at,updated_at,is_hazmat,revenue,weigth_lbs,status,driver_id,route_id) SELECT gen_random_uuid(),NOW(),NOW(),'t',1,0,'DELIVERED',(SELECT  id FROM auth_user WHERE email='trifun@trifun.com'), id FROM dispatch_route WHERE distance_miles = 71;

--     -- Load from Chicago to Milwaukee using 'distance_miles' as the unique field for the selection.--
--     -- WILLIAM is the driver for stefy --
--     INSERT INTO dispatch_load(id,created_at,updated_at,is_hazmat,revenue,weigth_lbs,status,driver_id,truck_id,route_id) SELECT gen_random_uuid(),NOW(),NOW(),'t',15,90,'ON ROAD',(SELECT  id FROM auth_user WHERE email='billylkms@gmail.com'), (SELECT id FROM equipment_management_truck WHERE vin='1FUJHHDR0NLNB5627'), id FROM dispatch_route WHERE distance_miles = 69;
    
--     -- Load from Rockford to Burlington  using 'distance_miles' as the unique field for the selection.--
--     -- WILLIAM is the driver for stefy --
--     INSERT INTO dispatch_load(id,created_at,updated_at,is_hazmat,revenue,weigth_lbs,status,driver_id,truck_id,route_id) SELECT gen_random_uuid(),NOW(),NOW(),'t',1,0,'DELIVERED',(SELECT  id FROM auth_user WHERE email='billylkms@gmail.com'), (SELECT id FROM equipment_management_truck WHERE vin='1FUJHHDR0NLNB5627'), id FROM dispatch_route WHERE distance_miles = 70;
