-- Valentina Studio --
-- MySQL dump --
-- ---------------------------------------------------------


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
-- ---------------------------------------------------------


-- CREATE TABLE "auth_group" -----------------------------------
CREATE TABLE `auth_group`( 
	`id` Int( 0 ) AUTO_INCREMENT NOT NULL,
	`name` VarChar( 150 ) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
	PRIMARY KEY ( `id` ),
	CONSTRAINT `name` UNIQUE( `name` ) )
CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
ENGINE = InnoDB
AUTO_INCREMENT = 1;
-- -------------------------------------------------------------


-- CREATE TABLE "auth_group_permissions" -----------------------
CREATE TABLE `auth_group_permissions`( 
	`id` BigInt( 0 ) AUTO_INCREMENT NOT NULL,
	`group_id` Int( 0 ) NOT NULL,
	`permission_id` Int( 0 ) NOT NULL,
	PRIMARY KEY ( `id` ),
	CONSTRAINT `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` UNIQUE( `group_id`, `permission_id` ) )
CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
ENGINE = InnoDB
AUTO_INCREMENT = 1;
-- -------------------------------------------------------------


-- CREATE TABLE "auth_permission" ------------------------------
CREATE TABLE `auth_permission`( 
	`id` Int( 0 ) AUTO_INCREMENT NOT NULL,
	`name` VarChar( 255 ) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
	`content_type_id` Int( 0 ) NOT NULL,
	`codename` VarChar( 100 ) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
	PRIMARY KEY ( `id` ),
	CONSTRAINT `auth_permission_content_type_id_codename_01ab375a_uniq` UNIQUE( `content_type_id`, `codename` ) )
CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
ENGINE = InnoDB
AUTO_INCREMENT = 29;
-- -------------------------------------------------------------


-- CREATE TABLE "auth_user" ------------------------------------
CREATE TABLE `auth_user`( 
	`id` Int( 0 ) AUTO_INCREMENT NOT NULL,
	`password` VarChar( 128 ) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
	`last_login` DateTime NULL DEFAULT NULL,
	`is_superuser` TinyInt( 1 ) NOT NULL,
	`username` VarChar( 150 ) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
	`first_name` VarChar( 150 ) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
	`last_name` VarChar( 150 ) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
	`email` VarChar( 254 ) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
	`is_staff` TinyInt( 1 ) NOT NULL,
	`is_active` TinyInt( 1 ) NOT NULL,
	`date_joined` DateTime NOT NULL,
	PRIMARY KEY ( `id` ),
	CONSTRAINT `username` UNIQUE( `username` ) )
CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
ENGINE = InnoDB
AUTO_INCREMENT = 1;
-- -------------------------------------------------------------


-- CREATE TABLE "auth_user_groups" -----------------------------
CREATE TABLE `auth_user_groups`( 
	`id` BigInt( 0 ) AUTO_INCREMENT NOT NULL,
	`user_id` Int( 0 ) NOT NULL,
	`group_id` Int( 0 ) NOT NULL,
	PRIMARY KEY ( `id` ),
	CONSTRAINT `auth_user_groups_user_id_group_id_94350c0c_uniq` UNIQUE( `user_id`, `group_id` ) )
CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
ENGINE = InnoDB
AUTO_INCREMENT = 1;
-- -------------------------------------------------------------


-- CREATE TABLE "auth_user_user_permissions" -------------------
CREATE TABLE `auth_user_user_permissions`( 
	`id` BigInt( 0 ) AUTO_INCREMENT NOT NULL,
	`user_id` Int( 0 ) NOT NULL,
	`permission_id` Int( 0 ) NOT NULL,
	PRIMARY KEY ( `id` ),
	CONSTRAINT `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` UNIQUE( `user_id`, `permission_id` ) )
CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
ENGINE = InnoDB
AUTO_INCREMENT = 1;
-- -------------------------------------------------------------


-- CREATE TABLE "django_admin_log" -----------------------------
CREATE TABLE `django_admin_log`( 
	`id` Int( 0 ) AUTO_INCREMENT NOT NULL,
	`action_time` DateTime NOT NULL,
	`object_id` LongText CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
	`object_repr` VarChar( 200 ) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
	`action_flag` SmallInt( 0 ) UNSIGNED NOT NULL,
	`change_message` LongText CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
	`content_type_id` Int( 0 ) NULL DEFAULT NULL,
	`user_id` Int( 0 ) NOT NULL,
	PRIMARY KEY ( `id` ) )
CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
ENGINE = InnoDB
AUTO_INCREMENT = 1;
-- -------------------------------------------------------------


-- CREATE TABLE "django_content_type" --------------------------
CREATE TABLE `django_content_type`( 
	`id` Int( 0 ) AUTO_INCREMENT NOT NULL,
	`app_label` VarChar( 100 ) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
	`model` VarChar( 100 ) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
	PRIMARY KEY ( `id` ),
	CONSTRAINT `django_content_type_app_label_model_76bd3d3b_uniq` UNIQUE( `app_label`, `model` ) )
CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
ENGINE = InnoDB
AUTO_INCREMENT = 8;
-- -------------------------------------------------------------


-- CREATE TABLE "django_migrations" ----------------------------
CREATE TABLE `django_migrations`( 
	`id` BigInt( 0 ) AUTO_INCREMENT NOT NULL,
	`app` VarChar( 255 ) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
	`name` VarChar( 255 ) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
	`applied` DateTime NOT NULL,
	PRIMARY KEY ( `id` ) )
CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
ENGINE = InnoDB
AUTO_INCREMENT = 21;
-- -------------------------------------------------------------


-- CREATE TABLE "django_session" -------------------------------
CREATE TABLE `django_session`( 
	`session_key` VarChar( 40 ) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
	`session_data` LongText CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
	`expire_date` DateTime NOT NULL,
	PRIMARY KEY ( `session_key` ) )
CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
ENGINE = InnoDB;
-- -------------------------------------------------------------


-- CREATE TABLE "django_site" ----------------------------------
CREATE TABLE `django_site`( 
	`id` Int( 0 ) AUTO_INCREMENT NOT NULL,
	`domain` VarChar( 100 ) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
	`name` VarChar( 50 ) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
	PRIMARY KEY ( `id` ),
	CONSTRAINT `django_site_domain_a2e37b91_uniq` UNIQUE( `domain` ) )
CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
ENGINE = InnoDB
AUTO_INCREMENT = 2;
-- -------------------------------------------------------------


-- CREATE TABLE "user_profile_profile" -------------------------
CREATE TABLE `user_profile_profile`( 
	`id` BigInt( 0 ) AUTO_INCREMENT NOT NULL,
	`profile_img` VarChar( 100 ) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
	`nickname` VarChar( 100 ) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
	`micro_value_lvl` Int( 0 ) NOT NULL,
	`micro_index` Int( 0 ) NOT NULL,
	`webcam_index` Int( 0 ) NOT NULL,
	`related_user_id` Int( 0 ) NOT NULL,
	PRIMARY KEY ( `id` ),
	CONSTRAINT `related_user_id` UNIQUE( `related_user_id` ) )
CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
ENGINE = InnoDB
AUTO_INCREMENT = 2;
-- -------------------------------------------------------------


-- Dump data of "auth_group" -------------------------------
-- ---------------------------------------------------------


-- Dump data of "auth_group_permissions" -------------------
-- ---------------------------------------------------------


-- Dump data of "auth_permission" --------------------------
BEGIN;

INSERT INTO `auth_permission`(`id`,`name`,`content_type_id`,`codename`) VALUES 
( '1', 'Can add log entry', '1', 'add_logentry' ),
( '2', 'Can change log entry', '1', 'change_logentry' ),
( '3', 'Can delete log entry', '1', 'delete_logentry' ),
( '4', 'Can view log entry', '1', 'view_logentry' ),
( '5', 'Can add permission', '2', 'add_permission' ),
( '6', 'Can change permission', '2', 'change_permission' ),
( '7', 'Can delete permission', '2', 'delete_permission' ),
( '8', 'Can view permission', '2', 'view_permission' ),
( '9', 'Can add group', '3', 'add_group' ),
( '10', 'Can change group', '3', 'change_group' ),
( '11', 'Can delete group', '3', 'delete_group' ),
( '12', 'Can view group', '3', 'view_group' ),
( '13', 'Can add user', '4', 'add_user' ),
( '14', 'Can change user', '4', 'change_user' ),
( '15', 'Can delete user', '4', 'delete_user' ),
( '16', 'Can view user', '4', 'view_user' ),
( '17', 'Can add site', '5', 'add_site' ),
( '18', 'Can change site', '5', 'change_site' ),
( '19', 'Can delete site', '5', 'delete_site' ),
( '20', 'Can view site', '5', 'view_site' ),
( '21', 'Can add content type', '6', 'add_contenttype' ),
( '22', 'Can change content type', '6', 'change_contenttype' ),
( '23', 'Can delete content type', '6', 'delete_contenttype' ),
( '24', 'Can view content type', '6', 'view_contenttype' ),
( '25', 'Can add session', '7', 'add_session' ),
( '26', 'Can change session', '7', 'change_session' ),
( '27', 'Can delete session', '7', 'delete_session' ),
( '28', 'Can view session', '7', 'view_session' ),
( '29', 'Can add user profile', '8', 'add_userprofile' ),
( '30', 'Can change user profile', '8', 'change_userprofile' ),
( '31', 'Can delete user profile', '8', 'delete_userprofile' ),
( '32', 'Can view user profile', '8', 'view_userprofile' ),
( '33', 'Can add profile', '9', 'add_profile' ),
( '34', 'Can change profile', '9', 'change_profile' ),
( '35', 'Can delete profile', '9', 'delete_profile' ),
( '36', 'Can view profile', '9', 'view_profile' );
COMMIT;
-- ---------------------------------------------------------


-- Dump data of "auth_user" --------------------------------
BEGIN;

INSERT INTO `auth_user`(`id`,`password`,`last_login`,`is_superuser`,`username`,`first_name`,`last_name`,`email`,`is_staff`,`is_active`,`date_joined`) VALUES 
( '2', 'pbkdf2_sha256$390000$e7MfcOCS2Vba0z0A4gJ470$ttBxSA1s6mTjsO3ilzZmfSCwuS7JMb8rKa74QnJPN08=', '2023-05-16 20:54:07.617282', '1', 'root', '', '', 'pasvas03@gmail.com', '1', '1', '2023-05-16 17:27:54.675082' ),
( '6', 'pbkdf2_sha256$390000$HHSRMjQDq1lirZovwJ9ENm$v6GIIo4eGUyD7BIVkTYB7Y/PaWOr1boMXYc+F9owZ7s=', '2023-05-16 20:56:57.255184', '0', 'o718b02', '', '', 'pasha2003vasenin@gmail.com', '0', '1', '2023-05-16 20:56:15.198380' );
COMMIT;
-- ---------------------------------------------------------


-- Dump data of "auth_user_groups" -------------------------
-- ---------------------------------------------------------


-- Dump data of "auth_user_user_permissions" ---------------
-- ---------------------------------------------------------


-- Dump data of "django_admin_log" -------------------------
BEGIN;

INSERT INTO `django_admin_log`(`id`,`action_time`,`object_id`,`object_repr`,`action_flag`,`change_message`,`content_type_id`,`user_id`) VALUES 
( '1', '2023-05-16 17:28:34.043657', '1', 'o718b02', '3', '', '4', '2' ),
( '2', '2023-05-16 20:31:38.788980', '3', 'o718b02', '3', '', '4', '2' ),
( '3', '2023-05-16 20:54:15.926105', '4', 'o718b02', '3', '', '4', '2' ),
( '4', '2023-05-16 20:55:55.102178', '5', 'o718b02', '3', '', '4', '2' );
COMMIT;
-- ---------------------------------------------------------


-- Dump data of "django_content_type" ----------------------
BEGIN;

INSERT INTO `django_content_type`(`id`,`app_label`,`model`) VALUES 
( '1', 'admin', 'logentry' ),
( '3', 'auth', 'group' ),
( '2', 'auth', 'permission' ),
( '4', 'auth', 'user' ),
( '6', 'contenttypes', 'contenttype' ),
( '7', 'sessions', 'session' ),
( '5', 'sites', 'site' ),
( '9', 'user_profile', 'profile' ),
( '8', 'user_profile', 'userprofile' );
COMMIT;
-- ---------------------------------------------------------


-- Dump data of "django_migrations" ------------------------
BEGIN;

INSERT INTO `django_migrations`(`id`,`app`,`name`,`applied`) VALUES 
( '1', 'contenttypes', '0001_initial', '2023-05-16 16:28:59.079598' ),
( '2', 'auth', '0001_initial', '2023-05-16 16:28:59.294963' ),
( '3', 'admin', '0001_initial', '2023-05-16 16:28:59.385963' ),
( '4', 'admin', '0002_logentry_remove_auto_add', '2023-05-16 16:28:59.392637' ),
( '5', 'admin', '0003_logentry_add_action_flag_choices', '2023-05-16 16:28:59.398620' ),
( '6', 'contenttypes', '0002_remove_content_type_name', '2023-05-16 16:28:59.449911' ),
( '7', 'auth', '0002_alter_permission_name_max_length', '2023-05-16 16:28:59.485959' ),
( '8', 'auth', '0003_alter_user_email_max_length', '2023-05-16 16:28:59.501324' ),
( '9', 'auth', '0004_alter_user_username_opts', '2023-05-16 16:28:59.507304' ),
( '10', 'auth', '0005_alter_user_last_login_null', '2023-05-16 16:28:59.531891' ),
( '11', 'auth', '0006_require_contenttypes_0002', '2023-05-16 16:28:59.533880' ),
( '12', 'auth', '0007_alter_validators_add_error_messages', '2023-05-16 16:28:59.538863' ),
( '13', 'auth', '0008_alter_user_username_max_length', '2023-05-16 16:28:59.565229' ),
( '14', 'auth', '0009_alter_user_last_name_max_length', '2023-05-16 16:28:59.590584' ),
( '15', 'auth', '0010_alter_group_name_max_length', '2023-05-16 16:28:59.603060' ),
( '16', 'auth', '0011_update_proxy_permissions', '2023-05-16 16:28:59.609040' ),
( '17', 'auth', '0012_alter_user_first_name_max_length', '2023-05-16 16:28:59.636006' ),
( '18', 'sessions', '0001_initial', '2023-05-16 16:28:59.654792' ),
( '19', 'sites', '0001_initial', '2023-05-16 16:28:59.665005' ),
( '20', 'sites', '0002_alter_domain_unique', '2023-05-16 16:28:59.675969' ),
( '21', 'user_profile', '0001_initial', '2023-05-16 17:25:22.427279' ),
( '22', 'user_profile', '0002_profile_delete_userprofile', '2023-05-16 20:53:34.815704' );
COMMIT;
-- ---------------------------------------------------------


-- Dump data of "django_session" ---------------------------
BEGIN;

INSERT INTO `django_session`(`session_key`,`session_data`,`expire_date`) VALUES 
( 'tp6tr56s0c4snvdi1f9ski2gw5rkdy1q', '.eJxVjMsOwiAQRf-FtSEEGR4u3fsNZAYGqRpISrsy_rtt0oVuzzn3vkXEdalxHTzHKYuLsOL0ywjTk9su8gPbvcvU2zJPJPdEHnbIW8_8uh7t30HFUbc1K9CsDVkPELTmkj16lVVCX2DDQMUZApVKYQ3ehWDPOmF2KRg2QOLzBebLOBw:1pz1j7:NoGJ--qnKT7-NNK0WFQf49Lz8p4yO02hIujc01qPeMg', '2023-05-30 20:56:57.257182' );
COMMIT;
-- ---------------------------------------------------------


-- Dump data of "django_site" ------------------------------
BEGIN;

INSERT INTO `django_site`(`id`,`domain`,`name`) VALUES 
( '1', 'example.com', 'example.com' );
COMMIT;
-- ---------------------------------------------------------


-- Dump data of "user_profile_profile" ---------------------
BEGIN;

INSERT INTO `user_profile_profile`(`id`,`profile_img`,`nickname`,`micro_value_lvl`,`micro_index`,`webcam_index`,`related_user_id`) VALUES 
( '1', 'profileImg/AnonIcon.png', 'гомик', '50', '0', '0', '6' );
COMMIT;
-- ---------------------------------------------------------


-- CREATE INDEX "auth_group_permissio_permission_id_84c5c92e_fk_auth_perm" 
CREATE INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` USING BTREE ON `auth_group_permissions`( `permission_id` );
-- -------------------------------------------------------------


-- CREATE INDEX "auth_user_groups_group_id_97559544_fk_auth_group_id" 
CREATE INDEX `auth_user_groups_group_id_97559544_fk_auth_group_id` USING BTREE ON `auth_user_groups`( `group_id` );
-- -------------------------------------------------------------


-- CREATE INDEX "auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm" 
CREATE INDEX `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` USING BTREE ON `auth_user_user_permissions`( `permission_id` );
-- -------------------------------------------------------------


-- CREATE INDEX "django_admin_log_content_type_id_c4bce8eb_fk_django_co" 
CREATE INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co` USING BTREE ON `django_admin_log`( `content_type_id` );
-- -------------------------------------------------------------


-- CREATE INDEX "django_admin_log_user_id_c564eba6_fk_auth_user_id" 
CREATE INDEX `django_admin_log_user_id_c564eba6_fk_auth_user_id` USING BTREE ON `django_admin_log`( `user_id` );
-- -------------------------------------------------------------


-- CREATE INDEX "django_session_expire_date_a5c62663" ----------
CREATE INDEX `django_session_expire_date_a5c62663` USING BTREE ON `django_session`( `expire_date` );
-- -------------------------------------------------------------


-- CREATE LINK "auth_group_permissions_group_id_b120cbf9_fk_auth_group_id" 
ALTER TABLE `auth_group_permissions`
	ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY ( `group_id` )
	REFERENCES `auth_group`( `id` )
	ON DELETE No Action
	ON UPDATE No Action;
-- -------------------------------------------------------------


-- CREATE LINK "auth_group_permissio_permission_id_84c5c92e_fk_auth_perm" 
ALTER TABLE `auth_group_permissions`
	ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY ( `permission_id` )
	REFERENCES `auth_permission`( `id` )
	ON DELETE No Action
	ON UPDATE No Action;
-- -------------------------------------------------------------


-- CREATE LINK "auth_permission_content_type_id_2f476e4b_fk_django_co" 
ALTER TABLE `auth_permission`
	ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY ( `content_type_id` )
	REFERENCES `django_content_type`( `id` )
	ON DELETE No Action
	ON UPDATE No Action;
-- -------------------------------------------------------------


-- CREATE LINK "auth_user_groups_group_id_97559544_fk_auth_group_id" 
ALTER TABLE `auth_user_groups`
	ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY ( `group_id` )
	REFERENCES `auth_group`( `id` )
	ON DELETE No Action
	ON UPDATE No Action;
-- -------------------------------------------------------------


-- CREATE LINK "auth_user_groups_user_id_6a12ed8b_fk_auth_user_id" 
ALTER TABLE `auth_user_groups`
	ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY ( `user_id` )
	REFERENCES `auth_user`( `id` )
	ON DELETE No Action
	ON UPDATE No Action;
-- -------------------------------------------------------------


-- CREATE LINK "auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id" 
ALTER TABLE `auth_user_user_permissions`
	ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY ( `user_id` )
	REFERENCES `auth_user`( `id` )
	ON DELETE No Action
	ON UPDATE No Action;
-- -------------------------------------------------------------


-- CREATE LINK "auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm" 
ALTER TABLE `auth_user_user_permissions`
	ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY ( `permission_id` )
	REFERENCES `auth_permission`( `id` )
	ON DELETE No Action
	ON UPDATE No Action;
-- -------------------------------------------------------------


-- CREATE LINK "django_admin_log_content_type_id_c4bce8eb_fk_django_co" 
ALTER TABLE `django_admin_log`
	ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY ( `content_type_id` )
	REFERENCES `django_content_type`( `id` )
	ON DELETE No Action
	ON UPDATE No Action;
-- -------------------------------------------------------------


-- CREATE LINK "django_admin_log_user_id_c564eba6_fk_auth_user_id" 
ALTER TABLE `django_admin_log`
	ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY ( `user_id` )
	REFERENCES `auth_user`( `id` )
	ON DELETE No Action
	ON UPDATE No Action;
-- -------------------------------------------------------------


-- CREATE LINK "user_profile_profile_related_user_id_9fdec873_fk_auth_user_id" 
ALTER TABLE `user_profile_profile`
	ADD CONSTRAINT `user_profile_profile_related_user_id_9fdec873_fk_auth_user_id` FOREIGN KEY ( `related_user_id` )
	REFERENCES `auth_user`( `id` )
	ON DELETE No Action
	ON UPDATE No Action;
-- -------------------------------------------------------------


/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
-- ---------------------------------------------------------


