-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 16, 2023 at 10:07 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dormdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add room', 7, 'add_room'),
(26, 'Can change room', 7, 'change_room'),
(27, 'Can delete room', 7, 'delete_room'),
(28, 'Can view room', 7, 'view_room'),
(29, 'Can add service', 8, 'add_service'),
(30, 'Can change service', 8, 'change_service'),
(31, 'Can delete service', 8, 'delete_service'),
(32, 'Can view service', 8, 'view_service'),
(33, 'Can add bed', 9, 'add_bed'),
(34, 'Can change bed', 9, 'change_bed'),
(35, 'Can delete bed', 9, 'delete_bed'),
(36, 'Can view bed', 9, 'view_bed'),
(37, 'Can add user', 10, 'add_user'),
(38, 'Can change user', 10, 'change_user'),
(39, 'Can delete user', 10, 'delete_user'),
(40, 'Can view user', 10, 'view_user'),
(41, 'Can add person', 11, 'add_person'),
(42, 'Can change person', 11, 'change_person'),
(43, 'Can delete person', 11, 'delete_person'),
(44, 'Can view person', 11, 'view_person'),
(45, 'Can add bed price history', 12, 'add_bedpricehistory'),
(46, 'Can change bed price history', 12, 'change_bedpricehistory'),
(47, 'Can delete bed price history', 12, 'delete_bedpricehistory'),
(48, 'Can view bed price history', 12, 'view_bedpricehistory'),
(49, 'Can add occupant', 13, 'add_occupant'),
(50, 'Can change occupant', 13, 'change_occupant'),
(51, 'Can delete occupant', 13, 'delete_occupant'),
(52, 'Can view occupant', 13, 'view_occupant'),
(53, 'Can add bill', 14, 'add_bill'),
(54, 'Can change bill', 14, 'change_bill'),
(55, 'Can delete bill', 14, 'delete_bill'),
(56, 'Can view bill', 14, 'view_bill'),
(57, 'Can add bill_ details', 15, 'add_bill_details'),
(58, 'Can change bill_ details', 15, 'change_bill_details'),
(59, 'Can delete bill_ details', 15, 'delete_bill_details'),
(60, 'Can view bill_ details', 15, 'view_bill_details'),
(61, 'Can add payment', 16, 'add_payment'),
(62, 'Can change payment', 16, 'change_payment'),
(63, 'Can delete payment', 16, 'delete_payment'),
(64, 'Can view payment', 16, 'view_payment'),
(65, 'Can add demerit', 17, 'add_demerit'),
(66, 'Can change demerit', 17, 'change_demerit'),
(67, 'Can delete demerit', 17, 'delete_demerit'),
(68, 'Can view demerit', 17, 'view_demerit'),
(69, 'Can add occupant demerit', 18, 'add_occupantdemerit'),
(70, 'Can change occupant demerit', 18, 'change_occupantdemerit'),
(71, 'Can delete occupant demerit', 18, 'delete_occupantdemerit'),
(72, 'Can view occupant demerit', 18, 'view_occupantdemerit'),
(73, 'Can add admin', 19, 'add_admin'),
(74, 'Can change admin', 19, 'change_admin'),
(75, 'Can delete admin', 19, 'delete_admin'),
(76, 'Can view admin', 19, 'view_admin');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$260000$NKET4h09l0rGdLSLxUILX0$ZqKTQOdvOIr5IXGJV9PrJn/sS6e70og8160m22U6uCs=', '2023-04-16 18:38:43.565393', 1, 'Carlo', '', '', 'redpuddin417@gmail.com', 1, 1, '2023-04-16 18:38:28.933245');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(19, 'dormitory', 'admin'),
(9, 'dormitory', 'bed'),
(12, 'dormitory', 'bedpricehistory'),
(14, 'dormitory', 'bill'),
(15, 'dormitory', 'bill_details'),
(17, 'dormitory', 'demerit'),
(13, 'dormitory', 'occupant'),
(18, 'dormitory', 'occupantdemerit'),
(16, 'dormitory', 'payment'),
(11, 'dormitory', 'person'),
(7, 'dormitory', 'room'),
(8, 'dormitory', 'service'),
(10, 'dormitory', 'user'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2023-04-10 07:36:26.182669'),
(2, 'auth', '0001_initial', '2023-04-10 07:36:27.008424'),
(3, 'admin', '0001_initial', '2023-04-10 07:36:27.186622'),
(4, 'admin', '0002_logentry_remove_auto_add', '2023-04-10 07:36:27.197818'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2023-04-10 07:36:27.210394'),
(6, 'contenttypes', '0002_remove_content_type_name', '2023-04-10 07:36:27.300366'),
(7, 'auth', '0002_alter_permission_name_max_length', '2023-04-10 07:36:27.379759'),
(8, 'auth', '0003_alter_user_email_max_length', '2023-04-10 07:36:27.400766'),
(9, 'auth', '0004_alter_user_username_opts', '2023-04-10 07:36:27.407847'),
(10, 'auth', '0005_alter_user_last_login_null', '2023-04-10 07:36:27.476918'),
(11, 'auth', '0006_require_contenttypes_0002', '2023-04-10 07:36:27.485670'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2023-04-10 07:36:27.498981'),
(13, 'auth', '0008_alter_user_username_max_length', '2023-04-10 07:36:27.560990'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2023-04-10 07:36:27.602401'),
(15, 'auth', '0010_alter_group_name_max_length', '2023-04-10 07:36:27.628814'),
(16, 'auth', '0011_update_proxy_permissions', '2023-04-10 07:36:27.681332'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2023-04-10 07:36:27.707660'),
(18, 'dormitory', '0001_initial', '2023-04-10 07:36:27.760735'),
(19, 'dormitory', '0002_service', '2023-04-10 07:36:27.814675'),
(20, 'dormitory', '0003_bed', '2023-04-10 07:36:27.873332'),
(21, 'dormitory', '0004_user', '2023-04-10 07:36:27.929787'),
(22, 'dormitory', '0005_alter_user_security_question_person', '2023-04-10 07:36:28.066991'),
(23, 'dormitory', '0006_bedpricehistory', '2023-04-10 07:36:28.195882'),
(24, 'dormitory', '0007_alter_service_base_amount', '2023-04-10 07:36:28.279438'),
(25, 'dormitory', '0008_occupant', '2023-04-10 07:36:28.552556'),
(26, 'dormitory', '0009_bill', '2023-04-10 07:36:28.788746'),
(27, 'dormitory', '0010_bill_details', '2023-04-10 07:36:28.989974'),
(28, 'dormitory', '0011_payment', '2023-04-10 07:36:29.113309'),
(29, 'dormitory', '0012_auto_20220928_1258', '2023-04-10 07:36:29.267126'),
(30, 'dormitory', '0013_auto_20220928_1305', '2023-04-10 07:36:29.316766'),
(31, 'dormitory', '0014_auto_20220929_0042', '2023-04-10 07:36:29.369924'),
(32, 'dormitory', '0015_alter_service_status', '2023-04-10 07:36:29.375123'),
(33, 'dormitory', '0016_auto_20220930_1455', '2023-04-10 07:36:29.809694'),
(34, 'dormitory', '0017_auto_20220930_1511', '2023-04-10 07:36:30.092021'),
(35, 'dormitory', '0018_auto_20220930_1512', '2023-04-10 07:36:30.099381'),
(36, 'dormitory', '0019_auto_20220930_1517', '2023-04-10 07:36:30.350126'),
(37, 'dormitory', '0020_auto_20220930_1520', '2023-04-10 07:36:30.439330'),
(38, 'dormitory', '0021_auto_20220930_1522', '2023-04-10 07:36:30.586910'),
(39, 'dormitory', '0022_auto_20221002_1248', '2023-04-10 07:36:30.709079'),
(40, 'dormitory', '0023_auto_20221004_0304', '2023-04-10 07:36:30.908965'),
(41, 'dormitory', '0024_auto_20221004_0312', '2023-04-10 07:36:31.023812'),
(42, 'dormitory', '0025_alter_person_middle_name', '2023-04-10 07:36:31.088785'),
(43, 'dormitory', '0026_alter_occupant_bedprice', '2023-04-10 07:36:31.297102'),
(44, 'dormitory', '0027_person_boarder_type', '2023-04-10 07:36:31.351411'),
(45, 'dormitory', '0028_auto_20221004_1041', '2023-04-10 07:36:31.573695'),
(46, 'dormitory', '0029_alter_bill_details_occupant', '2023-04-10 07:36:31.734608'),
(47, 'dormitory', '0030_alter_bill_details_description', '2023-04-10 07:36:31.889172'),
(48, 'dormitory', '0031_auto_20221006_1116', '2023-04-10 07:36:32.183221'),
(49, 'dormitory', '0032_auto_20221006_2212', '2023-04-10 07:36:32.242050'),
(50, 'dormitory', '0032_auto_20221006_2205', '2023-04-10 07:36:32.273787'),
(51, 'dormitory', '0033_merge_0032_auto_20221006_2205_0032_auto_20221006_2212', '2023-04-10 07:36:32.281796'),
(52, 'dormitory', '0034_auto_20221012_2138', '2023-04-10 07:36:32.338692'),
(53, 'dormitory', '0035_alter_bed_bed_code', '2023-04-10 07:36:32.349080'),
(54, 'dormitory', '0036_auto_20221013_1902', '2023-04-10 07:36:32.376396'),
(55, 'dormitory', '0037_alter_bed_bed_code', '2023-04-10 07:36:32.388119'),
(56, 'dormitory', '0038_alter_bed_bed_code', '2023-04-10 07:36:32.398861'),
(57, 'dormitory', '0039_alter_bed_bed_code', '2023-04-10 07:36:32.404905'),
(58, 'dormitory', '0040_alter_bed_bed_code', '2023-04-10 07:36:32.420462'),
(59, 'dormitory', '0041_remove_bed_bed_code', '2023-04-10 07:36:32.441342'),
(60, 'dormitory', '0042_bed_bed_code', '2023-04-10 07:36:32.477767'),
(61, 'dormitory', '0043_alter_bed_price', '2023-04-10 07:36:32.567020'),
(62, 'dormitory', '0044_alter_bed_price', '2023-04-10 07:36:32.655531'),
(63, 'dormitory', '0045_alter_person_gender', '2023-04-10 07:36:32.665380'),
(64, 'dormitory', '0035_alter_occupant_bedprice', '2023-04-10 07:36:32.738872'),
(65, 'dormitory', '0036_alter_bed_price', '2023-04-10 07:36:32.827982'),
(66, 'dormitory', '0046_merge_0036_alter_bed_price_0045_alter_person_gender', '2023-04-10 07:36:32.836079'),
(67, 'dormitory', '0047_alter_bed_price', '2023-04-10 07:36:33.016905'),
(68, 'dormitory', '0048_alter_room_floorlvl', '2023-04-10 07:36:33.026515'),
(69, 'dormitory', '0049_auto_20221020_0749', '2023-04-10 07:36:33.038968'),
(70, 'dormitory', '0050_auto_20221024_1348', '2023-04-10 07:36:33.052793'),
(71, 'dormitory', '0045_merge_0036_alter_bed_price_0044_alter_bed_price', '2023-04-10 07:36:33.060667'),
(72, 'dormitory', '0051_merge_20221031_1138', '2023-04-10 07:36:33.069963'),
(73, 'dormitory', '0052_auto_20221101_2004', '2023-04-10 07:36:33.137337'),
(74, 'dormitory', '0053_alter_person_reg_status', '2023-04-10 07:36:33.152860'),
(75, 'dormitory', '0054_alter_person_reg_status', '2023-04-10 07:36:33.218362'),
(76, 'dormitory', '0055_remove_person_reg_status', '2023-04-10 07:36:33.239005'),
(77, 'dormitory', '0056_person_reg_status', '2023-04-10 07:36:33.280602'),
(78, 'dormitory', '0057_auto_20221104_2135', '2023-04-10 07:36:33.334337'),
(79, 'dormitory', '0058_auto_20221107_1751', '2023-04-10 07:36:33.373068'),
(80, 'dormitory', '0059_auto_20221114_1317', '2023-04-10 07:36:33.422454'),
(81, 'dormitory', '0060_alter_bill_details_quantity', '2023-04-10 07:36:33.431981'),
(82, 'dormitory', '0061_remove_bill_details_quantity', '2023-04-10 07:36:33.464057'),
(83, 'dormitory', '0062_bill_details_quantity', '2023-04-10 07:36:33.506123'),
(84, 'dormitory', '0063_auto_20221118_1200', '2023-04-10 07:36:33.701649'),
(85, 'dormitory', '0064_alter_occupant_end_date', '2023-04-10 07:36:33.720462'),
(86, 'dormitory', '0065_alter_occupant_end_date', '2023-04-10 07:36:33.731456'),
(87, 'dormitory', '0066_auto_20221124_2126', '2023-04-10 07:36:33.866702'),
(88, 'dormitory', '0067_auto_20221127_0035', '2023-04-10 07:36:34.156499'),
(89, 'dormitory', '0068_auto_20221127_0045', '2023-04-10 07:36:34.286715'),
(90, 'dormitory', '0069_alter_demerit_demerit_name', '2023-04-10 07:36:34.296372'),
(91, 'dormitory', '0070_occupant_demerit', '2023-04-10 07:36:34.528207'),
(92, 'dormitory', '0071_rename_occupant_demerit_occupantdemerit', '2023-04-10 07:36:34.592702'),
(93, 'dormitory', '0072_auto_20221208_1520', '2023-04-10 07:36:34.890916'),
(94, 'dormitory', '0073_user_user_status', '2023-04-10 07:36:34.941455'),
(95, 'dormitory', '0074_alter_user_user_status', '2023-04-10 07:36:34.947450'),
(96, 'dormitory', '0075_user_person_id', '2023-04-10 07:36:34.965357'),
(97, 'dormitory', '0076_alter_user_user_status', '2023-04-10 07:36:34.979954'),
(98, 'dormitory', '0077_admin', '2023-04-10 07:36:35.083070'),
(99, 'dormitory', '0078_auto_20230102_1707', '2023-04-10 07:36:38.420102'),
(100, 'dormitory', '0079_auto_20230102_1714', '2023-04-10 07:36:38.460559'),
(101, 'dormitory', '0080_user_person_id', '2023-04-10 07:36:38.482632'),
(102, 'dormitory', '0081_alter_user_phone_number', '2023-04-10 07:36:38.678563'),
(103, 'dormitory', '0082_auto_20230102_2240', '2023-04-10 07:36:42.194614'),
(104, 'dormitory', '0083_delete_code', '2023-04-10 07:36:42.220754'),
(105, 'dormitory', '0084_alter_person_office_dept', '2023-04-10 07:36:42.284884'),
(106, 'dormitory', '0085_auto_20230105_1115', '2023-04-10 07:36:42.588327'),
(107, 'dormitory', '0086_delete_otpcode', '2023-04-10 07:36:42.605353'),
(108, 'dormitory', '0087_alter_demerit_demerit_points', '2023-04-10 07:36:42.634895'),
(109, 'dormitory', '0088_alter_person_contact_no', '2023-04-10 07:36:42.664716'),
(110, 'dormitory', '0089_auto_20230406_0033', '2023-04-10 07:36:42.691925'),
(111, 'dormitory', '0090_auto_20230406_1527', '2023-04-10 07:36:42.756878'),
(112, 'sessions', '0001_initial', '2023-04-10 07:36:42.807079'),
(113, 'dormitory', '0091_auto_20230413_0139', '2023-04-12 17:40:04.374399');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `dormitory_admin`
--

CREATE TABLE `dormitory_admin` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `lastname` varchar(100) NOT NULL,
  `firstname` varchar(100) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `security_question` varchar(250) DEFAULT NULL,
  `security_answer` varchar(250) DEFAULT NULL,
  `recovery_email` varchar(250) DEFAULT NULL,
  `admin_class` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `dormitory_admin`
--

INSERT INTO `dormitory_admin` (`id`, `created_at`, `updated_at`, `lastname`, `firstname`, `username`, `password`, `security_question`, `security_answer`, `recovery_email`, `admin_class`) VALUES
(1, '2023-04-15 15:58:53.014899', '2023-04-15 16:35:01.073845', 'sample', 'sample', 'sample', '123456789', 'In what city were you born?', 'sample', 'sample@gmail.com', 'Super Administrator'),
(2, '2023-04-16 10:23:44.259786', '2023-04-16 10:23:44.259786', 'sample2', 'sample2', 'frontdesk', '123456', 'In what city were you born?', 'sample', 'sample@gmail.com', 'Front Desk'),
(3, '2023-04-16 13:29:48.239633', '2023-04-16 13:29:48.239633', 'sample', 'sample', 'accounting', '123456', 'In what city were you born?', '123456', 'asssaas@gmail.com', 'Accounting Staff'),
(4, '2023-04-16 18:10:29.835292', '2023-04-16 18:10:29.835292', 'sample', 'sample', 'dormmanager', '123456', 'In what city were you born?', '123456', 'saassa@gmail.com', 'Dorm Manager');

-- --------------------------------------------------------

--
-- Table structure for table `dormitory_bed`
--

CREATE TABLE `dormitory_bed` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `price` decimal(6,2) NOT NULL,
  `bed_status` varchar(25) NOT NULL,
  `room_id` bigint(20) NOT NULL,
  `bed_code` varchar(25) NOT NULL,
  `bed_description` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `dormitory_bed`
--

INSERT INTO `dormitory_bed` (`id`, `created_at`, `updated_at`, `price`, `bed_status`, `room_id`, `bed_code`, `bed_description`) VALUES
(7, '2023-04-01 06:51:35.122448', '2023-04-01 06:51:35.122448', 1500.00, 'Vacant', 2, 'M1FR2-AU', 'Male Dorm, 1st Floor, Room 2, Bed A Upper deck.'),
(8, '2023-04-01 06:51:56.235672', '2023-04-01 06:51:56.235672', 1500.00, 'Vacant', 2, 'M1FR2-BL', 'Male Dorm, 1st Floor, Room 2, Bed B Lower deck.'),
(9, '2023-04-01 06:52:07.085190', '2023-04-01 06:52:07.085190', 1500.00, 'Vacant', 2, 'M1FR2-CU', 'Male Dorm, 1st Floor, Room 2, Bed C Upper deck.'),
(10, '2023-04-01 06:53:14.943068', '2023-04-01 06:53:14.943068', 1500.00, 'Vacant', 2, 'M1FR2-DL', 'Male Dorm, 1st Floor, Room 2, Bed D Lower deck.'),
(11, '2023-04-01 06:53:27.593957', '2023-04-01 06:53:27.593957', 1500.00, 'Vacant', 2, 'M1FR2-EU', 'Male Dorm, 1st Floor, Room 2, Bed E Upper deck.'),
(12, '2023-04-01 06:53:37.550068', '2023-04-01 06:53:37.550068', 1500.00, 'Vacant', 2, 'M1FR2-FL', 'Male Dorm, 1st Floor, Room 2, Bed F Lower deck.'),
(13, '2023-04-01 06:54:19.872233', '2023-04-01 06:54:19.872233', 1500.00, 'Vacant', 3, 'M1FR3-AU', 'Male Dorm, 1st Floor, Room 3, Bed A Upper deck.'),
(14, '2023-04-01 06:54:32.797594', '2023-04-01 06:54:32.797594', 1500.00, 'Vacant', 3, 'M1FR3-BL', 'Male Dorm, 1st Floor, Room 3, Bed B Lower deck.'),
(15, '2023-04-01 06:54:42.771024', '2023-04-01 06:54:42.771024', 1500.00, 'Vacant', 3, 'M1FR3-CU', 'Male Dorm, 1st Floor, Room 3, Bed C Upper deck.'),
(16, '2023-04-01 06:54:52.490307', '2023-04-01 06:54:52.490307', 1500.00, 'Vacant', 3, 'M1FR3-DL', 'Male Dorm, 1st Floor, Room 3, Bed D Lower deck.'),
(17, '2023-04-01 06:55:03.118671', '2023-04-01 06:55:03.118671', 1500.00, 'Vacant', 3, 'M1FR3-EU', 'Male Dorm, 1st Floor, Room 3, Bed E Upper deck.'),
(18, '2023-04-01 06:55:13.467383', '2023-04-01 06:55:13.467383', 1500.00, 'Vacant', 3, 'M1FR3-FL', 'Male Dorm, 1st Floor, Room 3, Bed F Lower deck.'),
(19, '2023-04-01 06:55:54.232288', '2023-04-01 06:55:54.232288', 1500.00, 'Vacant', 4, 'M1FR4-AU', 'Male Dorm, 1st Floor, Room 4, Bed A Upper deck.'),
(20, '2023-04-01 06:56:07.383472', '2023-04-01 06:56:07.383472', 1500.00, 'Vacant', 4, 'M1FR4-BL', 'Male Dorm, 1st Floor, Room 4, Bed B Lower deck.'),
(21, '2023-04-01 06:56:18.438410', '2023-04-01 06:56:18.438410', 1500.00, 'Vacant', 4, 'M1FR4-CU', 'Male Dorm, 1st Floor, Room 4, Bed C Upper deck.'),
(22, '2023-04-01 06:56:29.345531', '2023-04-01 06:56:29.345531', 1500.00, 'Vacant', 4, 'M1FR4-DL', 'Male Dorm, 1st Floor, Room 4, Bed D Lower deck.'),
(23, '2023-04-01 06:56:40.562138', '2023-04-01 06:56:40.562138', 1500.00, 'Vacant', 4, 'M1FR4-EU', 'Male Dorm, 1st Floor, Room 4, Bed E Upper deck.'),
(24, '2023-04-01 06:56:50.523619', '2023-04-01 06:56:50.523619', 1500.00, 'Vacant', 4, 'M1FR4-FL', 'Male Dorm, 1st Floor, Room 4, Bed F Lower deck.'),
(25, '2023-04-01 07:00:54.428847', '2023-04-01 07:00:54.428847', 1500.00, 'Vacant', 5, 'M1FR5-AU', 'Male Dorm, 1st Floor, Room 5, Bed A Upper deck.'),
(26, '2023-04-01 07:01:07.242391', '2023-04-01 07:01:07.242391', 1500.00, 'Vacant', 5, 'M1FR5-BL', 'Male Dorm, 1st Floor, Room 5, Bed B Lower deck.'),
(27, '2023-04-01 07:01:19.402695', '2023-04-01 07:01:19.402695', 1500.00, 'Vacant', 5, 'M1FR5-CU', 'Male Dorm, 1st Floor, Room 5, Bed C Upper deck.'),
(28, '2023-04-01 07:01:29.916015', '2023-04-01 07:01:29.916015', 1500.00, 'Vacant', 5, 'M1FR5-DL', 'Male Dorm, 1st Floor, Room 5, Bed D Lower deck.'),
(29, '2023-04-01 07:01:42.553560', '2023-04-01 07:01:42.553560', 1500.00, 'Vacant', 5, 'M1FR5-EU', 'Male Dorm, 1st Floor, Room 5, Bed E Upper deck.'),
(30, '2023-04-01 07:01:53.261838', '2023-04-01 07:01:53.261838', 1500.00, 'Vacant', 5, 'M1FR5-FL', 'Male Dorm, 1st Floor, Room 5, Bed F Lower deck.'),
(31, '2023-04-01 07:02:31.333313', '2023-04-01 07:02:31.333313', 1500.00, 'Vacant', 6, 'M1FR6-AU', 'Male Dorm, 1st Floor, Room 6, Bed A Upper deck.'),
(32, '2023-04-01 07:02:42.474671', '2023-04-01 07:02:42.474671', 1500.00, 'Vacant', 6, 'M1FR6-BL', 'Male Dorm, 1st Floor, Room 6, Bed B Lower deck.'),
(33, '2023-04-01 07:02:52.801376', '2023-04-01 07:02:52.801376', 1500.00, 'Vacant', 6, 'M1FR6-CU', 'Male Dorm, 1st Floor, Room 6, Bed C Upper deck.'),
(34, '2023-04-01 07:03:02.031490', '2023-04-01 07:03:02.031490', 1500.00, 'Vacant', 6, 'M1FR6-DL', 'Male Dorm, 1st Floor, Room 6, Bed D Lower deck.'),
(35, '2023-04-01 07:03:11.738141', '2023-04-01 07:03:11.738141', 1500.00, 'Vacant', 6, 'M1FR6-EU', 'Male Dorm, 1st Floor, Room 6, Bed E Upper deck.'),
(36, '2023-04-01 07:03:21.085995', '2023-04-01 07:03:21.085995', 1500.00, 'Vacant', 6, 'M1FR6-FL', 'Male Dorm, 1st Floor, Room 6, Bed F Lower deck.'),
(37, '2023-04-01 07:05:26.399212', '2023-04-01 07:05:26.399212', 1500.00, 'Vacant', 7, 'M1FR7-AU', 'Male Dorm, 1st Floor, Room 7, Bed A Upper deck.'),
(38, '2023-04-01 07:05:45.785894', '2023-04-01 07:05:45.785894', 1500.00, 'Vacant', 7, 'M1FR7-BL', 'Male Dorm, 1st Floor, Room 7, Bed B Lower deck.'),
(39, '2023-04-01 07:06:04.100803', '2023-04-01 07:06:04.100803', 1500.00, 'Vacant', 7, 'M1FR7-CU', 'Male Dorm, 1st Floor, Room 7, Bed C Upper deck.'),
(40, '2023-04-01 07:06:26.784457', '2023-04-01 07:06:26.784457', 1500.00, 'Vacant', 7, 'M1FR7-DL', 'Male Dorm, 1st Floor, Room 7, Bed D Lower deck.'),
(41, '2023-04-01 07:06:37.707544', '2023-04-01 07:06:37.707544', 1500.00, 'Vacant', 7, 'M1FR7-EU', 'Male Dorm, 1st Floor, Room 7, Bed E Upper deck.'),
(42, '2023-04-01 07:06:49.387373', '2023-04-01 07:06:49.387373', 1500.00, 'Vacant', 7, 'M1FR7-FL', 'Male Dorm, 1st Floor, Room 7, Bed F Lower deck.'),
(43, '2023-04-01 07:07:58.334477', '2023-04-01 07:07:58.334477', 1500.00, 'Vacant', 8, 'M1FR8-AU', 'Male Dorm, 1st Floor, Room 8, Bed A Upper deck.'),
(44, '2023-04-01 07:08:09.640477', '2023-04-01 07:08:09.640477', 1500.00, 'Vacant', 8, 'M1FR8-BL', 'Male Dorm, 1st Floor, Room 8, Bed B Lower deck.'),
(45, '2023-04-01 07:08:19.542204', '2023-04-01 07:08:19.542204', 1500.00, 'Vacant', 8, 'M1FR8-CU', 'Male Dorm, 1st Floor, Room 8, Bed C Upper deck.'),
(46, '2023-04-01 07:08:32.882479', '2023-04-01 07:08:32.882479', 1500.00, 'Vacant', 8, 'M1FR8-DL', 'Male Dorm, 1st Floor, Room 8, Bed D Lower deck.'),
(47, '2023-04-01 07:08:43.830782', '2023-04-01 07:08:43.830782', 1500.00, 'Vacant', 8, 'M1FR8-EU', 'Male Dorm, 1st Floor, Room 8, Bed E Upper deck.'),
(48, '2023-04-01 07:08:54.683548', '2023-04-01 07:08:54.683548', 1500.00, 'Vacant', 8, 'M1FR8-FL', 'Male Dorm, 1st Floor, Room 8, Bed F Lower deck.'),
(49, '2023-04-01 07:09:30.319822', '2023-04-01 07:09:30.319822', 1500.00, 'Vacant', 9, 'M1FR9-AU', 'Male Dorm, 1st Floor, Room 9, Bed A Upper deck.'),
(50, '2023-04-01 07:09:41.285556', '2023-04-01 07:11:04.369073', 1500.00, 'Vacant', 9, 'M1FR9-BL', 'Male Dorm, 1st Floor, Room 9, Bed B Lower deck.'),
(51, '2023-04-01 07:09:51.960174', '2023-04-01 07:09:51.960174', 1500.00, 'Vacant', 9, 'M1FR9-CU', 'Male Dorm, 1st Floor, Room 9, Bed C Upper deck.'),
(52, '2023-04-01 07:10:01.456962', '2023-04-01 07:10:01.456962', 1500.00, 'Vacant', 9, 'M1FR9-DL', 'Male Dorm, 1st Floor, Room 9, Bed D Lower deck.'),
(53, '2023-04-01 07:10:13.252957', '2023-04-01 07:10:13.252957', 1500.00, 'Vacant', 9, 'M1FR9-EU', 'Male Dorm, 1st Floor, Room 9, Bed E Upper deck.'),
(54, '2023-04-01 07:10:23.902317', '2023-04-01 07:10:23.902317', 1500.00, 'Vacant', 9, 'M1FR9-FL', 'Male Dorm, 1st Floor, Room 9, Bed F Lower deck.'),
(55, '2023-04-01 07:11:33.544371', '2023-04-01 07:11:33.544371', 1500.00, 'Vacant', 10, 'M1FR10-AU', 'Male Dorm, 1st Floor, Room 10, Bed A Upper deck.'),
(56, '2023-04-01 07:11:44.133114', '2023-04-01 07:11:44.133114', 1500.00, 'Vacant', 10, 'M1FR10-BL', 'Male Dorm, 1st Floor, Room 10, Bed B Lower deck.'),
(57, '2023-04-01 07:11:55.824015', '2023-04-01 07:11:55.824015', 1500.00, 'Vacant', 10, 'M1FR10-CU', 'Male Dorm, 1st Floor, Room 10, Bed C Upper deck.'),
(58, '2023-04-01 07:12:07.343072', '2023-04-01 07:12:07.343072', 1500.00, 'Vacant', 10, 'M1FR10-DL', 'Male Dorm, 1st Floor, Room 10, Bed D Lower deck.'),
(59, '2023-04-01 07:12:18.082874', '2023-04-01 07:12:18.082874', 1500.00, 'Vacant', 10, 'M1FR10-EU', 'Male Dorm, 1st Floor, Room 10, Bed E Upper deck.'),
(60, '2023-04-01 07:12:28.249070', '2023-04-01 07:12:28.249070', 1500.00, 'Vacant', 10, 'M1FR10-FL', 'Male Dorm, 1st Floor, Room 10, Bed F Lower deck.'),
(61, '2023-04-01 07:13:02.072832', '2023-04-01 07:13:02.072832', 1500.00, 'Vacant', 11, 'M2FR11-AU', 'Male Dorm, 2nd Floor, Room 11, Bed A Upper deck.'),
(62, '2023-04-01 07:13:29.115594', '2023-04-01 07:13:29.115594', 1500.00, 'Vacant', 11, 'M2FR11-BL', 'Male Dorm, 2nd Floor, Room 11, Bed B Lower deck.'),
(63, '2023-04-01 07:14:04.112123', '2023-04-01 07:14:04.112123', 1500.00, 'Vacant', 11, 'M2FR11-CU', 'Male Dorm, 2nd Floor, Room 11, Bed C Upper deck.'),
(64, '2023-04-01 07:14:15.640588', '2023-04-01 07:14:15.640588', 1500.00, 'Vacant', 11, 'M2FR11-DL', 'Male Dorm, 2nd Floor, Room 11, Bed D Lower deck.'),
(65, '2023-04-01 07:14:28.624997', '2023-04-01 07:14:28.624997', 1500.00, 'Vacant', 11, 'M2FR11-EU', 'Male Dorm, 2nd Floor, Room 11, Bed E Upper deck.'),
(66, '2023-04-01 07:14:38.973939', '2023-04-01 07:14:38.973939', 1500.00, 'Vacant', 11, 'M2FR11-FL', 'Male Dorm, 2nd Floor, Room 11, Bed F Lower deck.'),
(67, '2023-04-01 07:15:23.087351', '2023-04-01 07:15:23.087351', 1500.00, 'Vacant', 12, 'M2FR12-AU', 'Male Dorm, 2nd Floor, Room 12, Bed A Upper deck.'),
(68, '2023-04-01 07:15:36.360973', '2023-04-01 07:15:36.360973', 1500.00, 'Vacant', 12, 'M2FR12-BL', 'Male Dorm, 2nd Floor, Room 12, Bed B Lower deck.'),
(69, '2023-04-01 07:15:47.703714', '2023-04-01 07:15:47.703714', 1500.00, 'Vacant', 12, 'M2FR12-CU', 'Male Dorm, 2nd Floor, Room 12, Bed C Upper deck.'),
(70, '2023-04-01 07:15:58.178777', '2023-04-01 07:15:58.178777', 1500.00, 'Vacant', 12, 'M2FR12-DL', 'Male Dorm, 2nd Floor, Room 12, Bed D Lower deck.'),
(71, '2023-04-01 07:16:08.259424', '2023-04-01 07:16:08.259424', 1500.00, 'Vacant', 12, 'M2FR12-EU', 'Male Dorm, 2nd Floor, Room 12, Bed E Upper deck.'),
(72, '2023-04-01 07:16:18.053083', '2023-04-01 07:16:18.053083', 1500.00, 'Vacant', 12, 'M2FR12-FL', 'Male Dorm, 2nd Floor, Room 12, Bed F Lower deck.'),
(73, '2023-04-01 07:18:06.162148', '2023-04-01 07:18:06.162148', 1500.00, 'Vacant', 13, 'M2FR13-AU', 'Male Dorm, 2nd Floor, Room 13, Bed A Upper deck.'),
(74, '2023-04-01 07:18:20.703768', '2023-04-01 07:18:20.703768', 1500.00, 'Vacant', 13, 'M2FR13-BL', 'Male Dorm, 2nd Floor, Room 13, Bed B Lower deck.'),
(75, '2023-04-01 07:18:29.920994', '2023-04-01 07:18:29.920994', 1500.00, 'Vacant', 13, 'M2FR13-CU', 'Male Dorm, 2nd Floor, Room 13, Bed C Upper deck.'),
(76, '2023-04-01 07:18:39.019747', '2023-04-01 07:18:39.019747', 1500.00, 'Vacant', 13, 'M2FR13-DL', 'Male Dorm, 2nd Floor, Room 13, Bed D Lower deck.'),
(77, '2023-04-01 07:18:47.799470', '2023-04-01 07:18:47.799470', 1500.00, 'Vacant', 13, 'M2FR13-EU', 'Male Dorm, 2nd Floor, Room 13, Bed E Upper deck.'),
(78, '2023-04-01 07:18:58.310738', '2023-04-01 07:18:58.310738', 1500.00, 'Vacant', 13, 'M2FR13-FL', 'Male Dorm, 2nd Floor, Room 13, Bed F Lower deck.'),
(79, '2023-04-01 07:19:26.694177', '2023-04-01 07:19:26.694177', 1500.00, 'Vacant', 14, 'M2FR14-AU', 'Male Dorm, 2nd Floor, Room 14, Bed A Upper deck.'),
(80, '2023-04-01 07:19:36.352679', '2023-04-01 07:19:36.352679', 1500.00, 'Vacant', 14, 'M2FR14-BL', 'Male Dorm, 2nd Floor, Room 14, Bed B Lower deck.'),
(81, '2023-04-01 07:19:46.498889', '2023-04-01 07:19:46.498889', 1500.00, 'Vacant', 14, 'M2FR14-CU', 'Male Dorm, 2nd Floor, Room 14, Bed C Upper deck.'),
(82, '2023-04-01 07:20:48.978555', '2023-04-01 07:20:48.978555', 1500.00, 'Vacant', 14, 'M2FR14-DL', 'Male Dorm, 2nd Floor, Room 14, Bed D Lower deck.'),
(83, '2023-04-01 07:20:59.130590', '2023-04-01 07:20:59.131721', 1500.00, 'Vacant', 14, 'M2FR14-EU', 'Male Dorm, 2nd Floor, Room 14, Bed E Upper deck.'),
(84, '2023-04-01 07:21:08.943741', '2023-04-01 07:21:08.943741', 1500.00, 'Vacant', 14, 'M2FR14-FL', 'Male Dorm, 2nd Floor, Room 14, Bed F Lower deck.'),
(85, '2023-04-01 07:21:41.514951', '2023-04-01 07:21:41.514951', 1500.00, 'Vacant', 15, 'M2FR15-AU', 'Male Dorm, 2nd Floor, Room 15, Bed A Upper deck.'),
(86, '2023-04-01 07:21:53.954227', '2023-04-01 07:21:53.954227', 1500.00, 'Vacant', 15, 'M2FR15-BL', 'Male Dorm, 2nd Floor, Room 15, Bed B Lower deck.'),
(87, '2023-04-01 07:22:05.034290', '2023-04-01 07:22:05.034290', 1500.00, 'Vacant', 15, 'M2FR15-CU', 'Male Dorm, 2nd Floor, Room 15, Bed C Upper deck.'),
(88, '2023-04-01 07:22:15.640073', '2023-04-01 07:22:15.640073', 1500.00, 'Vacant', 15, 'M2FR15-DL', 'Male Dorm, 2nd Floor, Room 15, Bed D Lower deck.'),
(89, '2023-04-01 07:22:26.719287', '2023-04-01 07:22:26.719287', 1500.00, 'Vacant', 15, 'M2FR15-EU', 'Male Dorm, 2nd Floor, Room 15, Bed E Upper deck.'),
(90, '2023-04-01 07:22:36.914389', '2023-04-01 07:22:36.914389', 1500.00, 'Vacant', 15, 'M2FR15-FL', 'Male Dorm, 2nd Floor, Room 15, Bed F Lower deck.'),
(91, '2023-04-01 07:23:02.903488', '2023-04-01 07:23:02.903488', 1500.00, 'Vacant', 16, 'M2FR16-AU', 'Male Dorm, 2nd Floor, Room 16, Bed A Upper deck.'),
(92, '2023-04-01 07:23:13.033051', '2023-04-01 07:23:13.033051', 1500.00, 'Vacant', 16, 'M2FR16-BL', 'Male Dorm, 2nd Floor, Room 16, Bed B Lower deck.'),
(93, '2023-04-01 07:23:23.818121', '2023-04-01 07:23:23.818121', 1500.00, 'Vacant', 16, 'M2FR16-CU', 'Male Dorm, 2nd Floor, Room 16, Bed C Upper deck.'),
(94, '2023-04-01 07:23:35.350473', '2023-04-01 07:23:35.350473', 1500.00, 'Vacant', 16, 'M2FR16-DL', 'Male Dorm, 2nd Floor, Room 16, Bed D Lower deck.'),
(95, '2023-04-01 07:23:47.187823', '2023-04-01 07:23:47.187823', 1500.00, 'Vacant', 16, 'M2FR16-EU', 'Male Dorm, 2nd Floor, Room 16, Bed E Upper deck.'),
(96, '2023-04-01 07:23:56.492057', '2023-04-01 07:23:56.492057', 1500.00, 'Vacant', 16, 'M2FR16-FL', 'Male Dorm, 2nd Floor, Room 16, Bed F Lower deck.'),
(97, '2023-04-01 07:24:22.002217', '2023-04-01 07:24:22.002217', 1500.00, 'Vacant', 17, 'M2FR17-AU', 'Male Dorm, 2nd Floor, Room 17, Bed A Upper deck.'),
(98, '2023-04-01 07:24:32.094808', '2023-04-01 07:24:32.094808', 1500.00, 'Vacant', 17, 'M2FR17-BL', 'Male Dorm, 2nd Floor, Room 17, Bed B Lower deck.'),
(99, '2023-04-01 07:24:41.244076', '2023-04-01 07:24:41.244076', 1500.00, 'Vacant', 17, 'M2FR17-CU', 'Male Dorm, 2nd Floor, Room 17, Bed C Upper deck.'),
(100, '2023-04-01 07:24:51.377078', '2023-04-01 07:24:51.377078', 1500.00, 'Vacant', 17, 'M2FR17-DL', 'Male Dorm, 2nd Floor, Room 17, Bed D Lower deck.'),
(101, '2023-04-01 07:25:00.461019', '2023-04-01 07:25:00.461019', 1500.00, 'Vacant', 17, 'M2FR17-EU', 'Male Dorm, 2nd Floor, Room 17, Bed E Upper deck.'),
(102, '2023-04-01 07:25:10.043490', '2023-04-01 07:25:10.043490', 1500.00, 'Vacant', 17, 'M2FR17-FL', 'Male Dorm, 2nd Floor, Room 17, Bed F Lower deck.'),
(103, '2023-04-01 07:25:39.170961', '2023-04-01 07:25:39.170961', 1500.00, 'Vacant', 18, 'M2FR18-AU', 'Male Dorm, 2nd Floor, Room 18, Bed A Upper deck.'),
(104, '2023-04-01 07:25:48.685773', '2023-04-01 07:25:48.685773', 1500.00, 'Vacant', 18, 'M2FR18-BL', 'Male Dorm, 2nd Floor, Room 18, Bed B Lower deck.'),
(105, '2023-04-01 07:26:01.957573', '2023-04-01 07:26:01.957573', 1500.00, 'Vacant', 18, 'M2FR18-CU', 'Male Dorm, 2nd Floor, Room 18, Bed C Upper deck.'),
(106, '2023-04-01 07:26:13.657727', '2023-04-01 07:26:13.657727', 1500.00, 'Vacant', 18, 'M2FR18-DL', 'Male Dorm, 2nd Floor, Room 18, Bed D Lower deck.'),
(107, '2023-04-01 07:26:26.542141', '2023-04-01 07:26:26.542652', 1500.00, 'Vacant', 18, 'M2FR18-EU', 'Male Dorm, 2nd Floor, Room 18, Bed E Upper deck.'),
(108, '2023-04-01 07:26:36.708276', '2023-04-01 07:26:36.708276', 1500.00, 'Vacant', 18, 'M2FR18-FL', 'Male Dorm, 2nd Floor, Room 18, Bed F Lower deck.'),
(109, '2023-04-01 07:27:10.114556', '2023-04-01 07:27:10.114556', 1500.00, 'Vacant', 19, 'M2FR19-AU', 'Male Dorm, 2nd Floor, Room 19, Bed A Upper deck.'),
(110, '2023-04-01 07:27:22.227177', '2023-04-01 07:27:22.227177', 1500.00, 'Vacant', 19, 'M2FR19-BL', 'Male Dorm, 2nd Floor, Room 19, Bed B Lower deck.'),
(111, '2023-04-01 07:27:34.725977', '2023-04-01 07:27:34.729463', 1500.00, 'Vacant', 19, 'M2FR19-CU', 'Male Dorm, 2nd Floor, Room 19, Bed C Upper deck.'),
(112, '2023-04-01 07:27:45.317382', '2023-04-01 07:27:45.317382', 1500.00, 'Vacant', 19, 'M2FR19-DL', 'Male Dorm, 2nd Floor, Room 19, Bed D Lower deck.'),
(113, '2023-04-01 07:27:58.337525', '2023-04-01 07:27:58.337525', 1500.00, 'Vacant', 19, 'M2FR19-EU', 'Male Dorm, 2nd Floor, Room 19, Bed E Upper deck.'),
(114, '2023-04-01 07:28:08.735535', '2023-04-01 07:28:08.735535', 1500.00, 'Vacant', 19, 'M2FR19-FL', 'Male Dorm, 2nd Floor, Room 19, Bed F Lower deck.'),
(115, '2023-04-01 07:28:45.019565', '2023-04-01 07:28:45.020586', 1500.00, 'Vacant', 20, 'M2FR20-AU', 'Male Dorm, 2nd Floor, Room 20, Bed A Upper deck.'),
(116, '2023-04-01 07:28:57.221070', '2023-04-01 07:28:57.221070', 1500.00, 'Vacant', 20, 'M2FR20-BL', 'Male Dorm, 2nd Floor, Room 20, Bed B Lower deck.'),
(117, '2023-04-01 07:29:08.706723', '2023-04-01 07:29:08.706723', 1500.00, 'Vacant', 20, 'M2FR20-CU', 'Male Dorm, 2nd Floor, Room 20, Bed C Upper deck.'),
(118, '2023-04-01 07:29:19.745288', '2023-04-01 07:29:19.745288', 1500.00, 'Vacant', 20, 'M2FR20-DL', 'Male Dorm, 2nd Floor, Room 20, Bed D Lower deck.'),
(119, '2023-04-01 07:29:29.152482', '2023-04-01 07:29:29.152482', 1500.00, 'Vacant', 20, 'M2FR20-EU', 'Male Dorm, 2nd Floor, Room 20, Bed E Upper deck.'),
(120, '2023-04-01 07:29:41.306592', '2023-04-01 07:29:41.306592', 1500.00, 'Vacant', 20, 'M2FR20-FL', 'Male Dorm, 2nd Floor, Room 20, Bed F Lower deck.'),
(121, '2023-04-01 07:30:15.553114', '2023-04-01 07:30:15.553114', 1500.00, 'Vacant', 21, 'M2FR21-AU', 'Male Dorm, 2nd Floor, Room 21, Bed A Upper deck.'),
(122, '2023-04-01 07:30:27.267386', '2023-04-01 07:30:27.267386', 1500.00, 'Vacant', 21, 'M2FR21-BL', 'Male Dorm, 2nd Floor, Room 21, Bed B Lower deck.'),
(123, '2023-04-01 07:30:36.824330', '2023-04-01 07:30:36.824330', 1500.00, 'Vacant', 21, 'M2FR21-CU', 'Male Dorm, 2nd Floor, Room 21, Bed C Upper deck.'),
(124, '2023-04-01 07:30:46.548465', '2023-04-01 07:30:46.548465', 1500.00, 'Vacant', 21, 'M2FR21-DL', 'Male Dorm, 2nd Floor, Room 21, Bed D Lower deck.'),
(125, '2023-04-01 07:30:58.988015', '2023-04-01 07:30:58.988015', 1500.00, 'Vacant', 21, 'M2FR21-EU', 'Male Dorm, 2nd Floor, Room 21, Bed E Upper deck.'),
(126, '2023-04-01 07:31:09.546492', '2023-04-01 07:31:09.546492', 1500.00, 'Vacant', 21, 'M2FR21-FL', 'Male Dorm, 2nd Floor, Room 21, Bed F Lower deck.'),
(127, '2023-04-01 07:32:18.031869', '2023-04-01 07:32:18.031869', 1500.00, 'Vacant', 22, 'FM1FR1-AU', 'Female Dorm, 1st Floor, Room 1, Bed A Upper deck.'),
(128, '2023-04-01 07:32:28.725661', '2023-04-01 07:32:28.725661', 1500.00, 'Vacant', 22, 'FM1FR1-BL', 'Female Dorm, 1st Floor, Room 1, Bed B Lower deck.'),
(129, '2023-04-01 07:32:43.862020', '2023-04-01 07:32:43.864483', 1500.00, 'Vacant', 22, 'FM1FR1-CU', 'Female Dorm, 1st Floor, Room 1, Bed C Upper deck.'),
(130, '2023-04-01 07:33:01.411494', '2023-04-01 07:33:01.411494', 1500.00, 'Vacant', 22, 'FM1FR1-DL', 'Female Dorm, 1st Floor, Room 1, Bed D Lower deck.'),
(131, '2023-04-01 07:33:11.943223', '2023-04-01 07:33:11.943223', 1500.00, 'Vacant', 22, 'FM1FR1-EU', 'Female Dorm, 1st Floor, Room 1, Bed E Upper deck.'),
(132, '2023-04-01 07:33:22.132817', '2023-04-01 07:33:22.132817', 1500.00, 'Vacant', 22, 'FM1FR1-FL', 'Female Dorm, 1st Floor, Room 1, Bed F Lower deck.'),
(133, '2023-04-01 07:33:55.534581', '2023-04-01 07:33:55.534581', 1500.00, 'Vacant', 23, 'FM1FR2-AU', 'Female Dorm, 1st Floor, Room 2, Bed A Upper deck.'),
(134, '2023-04-01 07:34:07.104659', '2023-04-01 07:34:07.104659', 1500.00, 'Vacant', 23, 'FM1FR2-BL', 'Female Dorm, 1st Floor, Room 2, Bed B Lower deck.'),
(135, '2023-04-01 07:34:18.242649', '2023-04-01 07:34:18.242649', 1500.00, 'Vacant', 23, 'FM1FR2-CU', 'Female Dorm, 1st Floor, Room 2, Bed C Upper deck.'),
(136, '2023-04-01 07:34:29.818459', '2023-04-01 07:34:29.818459', 1500.00, 'Vacant', 23, 'FM1FR2-DL', 'Female Dorm, 1st Floor, Room 2, Bed D Lower deck.'),
(137, '2023-04-01 07:34:41.714744', '2023-04-01 07:34:41.714744', 1500.00, 'Vacant', 23, 'FM1FR2-EU', 'Female Dorm, 1st Floor, Room 2, Bed E Upper deck.'),
(138, '2023-04-01 07:34:57.418700', '2023-04-01 07:34:57.418700', 1500.00, 'Vacant', 23, 'FM1FR2-FL', 'Female Dorm, 1st Floor, Room 2, Bed F Lower deck.'),
(139, '2023-04-01 07:37:43.187264', '2023-04-01 07:37:43.187264', 1500.00, 'Vacant', 24, 'FM1FR3-AU', 'Female Dorm, 1st Floor, Room 3, Bed A Upper deck.'),
(140, '2023-04-01 07:38:13.575761', '2023-04-01 07:38:13.575761', 1500.00, 'Vacant', 24, 'FM1FR3-BL', 'Female Dorm, 1st Floor, Room 3, Bed B Lower deck.'),
(141, '2023-04-01 07:38:24.444703', '2023-04-01 07:38:24.444703', 1500.00, 'Vacant', 24, 'FM1FR3-CU', 'Female Dorm, 1st Floor, Room 3, Bed C Upper deck.'),
(142, '2023-04-01 07:38:36.455916', '2023-04-01 07:38:36.455916', 1500.00, 'Vacant', 24, 'FM1FR3-DL', 'Female Dorm, 1st Floor, Room 3, Bed D Lower deck.'),
(143, '2023-04-01 07:38:48.375657', '2023-04-01 07:38:48.375657', 1500.00, 'Vacant', 24, 'FM1FR3-EU', 'Female Dorm, 1st Floor, Room 3, Bed E Upper deck.'),
(144, '2023-04-01 07:39:00.644707', '2023-04-01 07:39:00.644707', 1500.00, 'Vacant', 24, 'FM1FR3-FL', 'Female Dorm, 1st Floor, Room 3, Bed F Lower deck.'),
(145, '2023-04-01 07:39:53.785659', '2023-04-01 07:39:53.785659', 1500.00, 'Vacant', 25, 'FM1FR4-AU', 'Female Dorm, 1st Floor, Room 4, Bed A Upper deck.'),
(146, '2023-04-01 07:40:09.910728', '2023-04-01 07:40:09.910728', 1500.00, 'Vacant', 25, 'FM1FR4-BL', 'Female Dorm, 1st Floor, Room 4, Bed B Lower deck.'),
(147, '2023-04-01 07:40:22.729217', '2023-04-01 07:40:22.729217', 1500.00, 'Vacant', 25, 'FM1FR4-CU', 'Female Dorm, 1st Floor, Room 4, Bed C Upper deck.'),
(148, '2023-04-01 07:40:39.556268', '2023-04-01 07:40:39.556268', 1500.00, 'Vacant', 25, 'FM1FR4-DL', 'Female Dorm, 1st Floor, Room 4, Bed D Lower deck.'),
(149, '2023-04-01 07:40:55.973356', '2023-04-01 07:40:55.973356', 1500.00, 'Vacant', 25, 'FM1FR4-EU', 'Female Dorm, 1st Floor, Room 4, Bed E Upper deck.'),
(150, '2023-04-01 07:41:08.415606', '2023-04-01 07:41:08.415606', 1500.00, 'Vacant', 25, 'FM1FR4-FL', 'Female Dorm, 1st Floor, Room 4, Bed F Lower deck.'),
(151, '2023-04-01 07:41:39.008938', '2023-04-01 07:41:39.008938', 1500.00, 'Vacant', 26, 'FM1FR5-AU', 'Female Dorm, 1st Floor, Room 5, Bed A Upper deck.'),
(152, '2023-04-01 07:41:54.703672', '2023-04-01 07:41:54.703672', 1500.00, 'Vacant', 26, 'FM1FR5-BL', 'Female Dorm, 1st Floor, Room 5, Bed B Lower deck.'),
(153, '2023-04-01 07:42:04.735360', '2023-04-01 07:42:04.735360', 1500.00, 'Vacant', 26, 'FM1FR5-CU', 'Female Dorm, 1st Floor, Room 5, Bed C Upper deck.'),
(154, '2023-04-01 07:42:16.602154', '2023-04-01 07:42:16.602154', 1500.00, 'Vacant', 26, 'FM1FR5-DL', 'Female Dorm, 1st Floor, Room 5, Bed D Lower deck.'),
(155, '2023-04-01 07:42:26.674875', '2023-04-01 07:42:26.674875', 1500.00, 'Vacant', 26, 'FM1FR5-EU', 'Female Dorm, 1st Floor, Room 5, Bed E Upper deck.'),
(156, '2023-04-01 07:42:39.504617', '2023-04-01 07:42:39.504617', 1500.00, 'Vacant', 26, 'FM1FR5-FL', 'Female Dorm, 1st Floor, Room 5, Bed F Lower deck.'),
(157, '2023-04-01 07:43:09.249035', '2023-04-01 07:43:09.249035', 1500.00, 'Vacant', 27, 'FM2FR6-AU', 'Female Dorm, 2nd Floor, Room 6, Bed A Upper deck.'),
(158, '2023-04-01 07:43:33.877623', '2023-04-01 07:43:33.877623', 1500.00, 'Vacant', 27, 'FM2FR6-BL', 'Female Dorm, 2nd Floor, Room 6, Bed B Lower deck.'),
(159, '2023-04-01 07:43:46.607322', '2023-04-01 07:43:46.607322', 1500.00, 'Vacant', 27, 'FM2FR6-CU', 'Female Dorm, 2nd Floor, Room 6, Bed C Upper deck.'),
(160, '2023-04-01 07:43:58.650514', '2023-04-01 07:43:58.650514', 1500.00, 'Vacant', 27, 'FM2FR6-DL', 'Female Dorm, 2nd Floor, Room 6, Bed D Lower deck.'),
(161, '2023-04-01 07:44:08.143888', '2023-04-01 07:44:08.143888', 1500.00, 'Vacant', 27, 'FM2FR6-EU', 'Female Dorm, 2nd Floor, Room 6, Bed E Upper deck.'),
(162, '2023-04-01 07:44:19.165727', '2023-04-01 07:44:19.165727', 1500.00, 'Vacant', 27, 'FM2FR6-FL', 'Female Dorm, 2nd Floor, Room 6, Bed F Lower deck.'),
(163, '2023-04-01 07:46:04.600895', '2023-04-01 07:46:04.600895', 1500.00, 'Vacant', 28, 'FM2FR7-AU', 'Female Dorm, 2nd Floor, Room 7, Bed A Upper deck.'),
(164, '2023-04-01 07:46:17.053663', '2023-04-01 07:46:17.053663', 1500.00, 'Vacant', 28, 'FM2FR7-BL', 'Female Dorm, 2nd Floor, Room 7, Bed B Lower deck.'),
(165, '2023-04-01 07:46:28.127190', '2023-04-01 07:46:28.127190', 1500.00, 'Vacant', 28, 'FM2FR7-CU', 'Female Dorm, 2nd Floor, Room 7, Bed C Upper deck.'),
(166, '2023-04-01 07:46:41.163910', '2023-04-01 07:46:41.163910', 1500.00, 'Vacant', 28, 'FM2FR7-DL', 'Female Dorm, 2nd Floor, Room 7, Bed D Lower deck.'),
(167, '2023-04-01 07:46:52.219891', '2023-04-01 07:46:52.219891', 1500.00, 'Vacant', 28, 'FM2FR7-EU', 'Female Dorm, 2nd Floor, Room 7, Bed E Upper deck.'),
(168, '2023-04-01 07:47:03.474115', '2023-04-01 07:47:03.474115', 1500.00, 'Vacant', 28, 'FM2FR7-FL', 'Female Dorm, 2nd Floor, Room 7, Bed F Lower deck.'),
(169, '2023-04-01 07:47:32.732860', '2023-04-01 07:47:32.732860', 1500.00, 'Vacant', 29, 'FM2FR8-AU', 'Female Dorm, 2nd Floor, Room 8, Bed A Upper deck.'),
(170, '2023-04-01 07:47:42.189440', '2023-04-01 07:47:42.189440', 1500.00, 'Vacant', 29, 'FM2FR8-BL', 'Female Dorm, 2nd Floor, Room 8, Bed B Lower deck.'),
(171, '2023-04-01 07:48:02.807393', '2023-04-01 07:48:02.807393', 1500.00, 'Vacant', 29, 'FM2FR8-CU', 'Female Dorm, 2nd Floor, Room 8, Bed C Upper deck.'),
(172, '2023-04-01 07:48:15.301139', '2023-04-01 07:48:15.301139', 1500.00, 'Vacant', 29, 'FM2FR8-DL', 'Female Dorm, 2nd Floor, Room 8, Bed D Lower deck.'),
(173, '2023-04-01 07:48:27.944374', '2023-04-01 07:48:27.944374', 1500.00, 'Vacant', 29, 'FM2FR8-EU', 'Female Dorm, 2nd Floor, Room 8, Bed E Upper deck.'),
(174, '2023-04-01 07:48:40.911124', '2023-04-01 07:48:40.911124', 1500.00, 'Vacant', 29, 'FM2FR8-FL', 'Female Dorm, 2nd Floor, Room 8, Bed F Lower deck.'),
(175, '2023-04-01 07:50:11.021035', '2023-04-01 07:50:11.021035', 1500.00, 'Vacant', 30, 'FM2FR9-AU', 'Female Dorm, 2nd Floor, Room 9, Bed A Upper deck.'),
(176, '2023-04-01 07:50:22.400627', '2023-04-01 07:50:22.400627', 1500.00, 'Vacant', 30, 'FM2FR9-BL', 'Female Dorm, 2nd Floor, Room 9, Bed B Lower deck.'),
(177, '2023-04-01 07:50:35.595638', '2023-04-01 07:50:35.595638', 1500.00, 'Vacant', 30, 'FM2FR9-CU', 'Female Dorm, 2nd Floor, Room 9, Bed C Upper deck.'),
(178, '2023-04-01 07:50:50.133504', '2023-04-01 07:50:50.133504', 1500.00, 'Vacant', 30, 'FM2FR9-DL', 'Female Dorm, 2nd Floor, Room 9, Bed D Lower deck.'),
(179, '2023-04-01 07:51:05.709803', '2023-04-01 07:51:05.709803', 1500.00, 'Vacant', 30, 'FM2FR9-EU', 'Female Dorm, 2nd Floor, Room 9, Bed E Upper deck.'),
(180, '2023-04-01 07:51:31.610936', '2023-04-01 07:51:31.610936', 1500.00, 'Vacant', 30, 'FM2FR9-FL', 'Female Dorm, 2nd Floor, Room 9, Bed F Lower deck.'),
(181, '2023-04-01 07:52:16.877300', '2023-04-01 07:52:16.877300', 1500.00, 'Vacant', 31, 'FM2FR10-AU', 'Female Dorm, 2nd Floor, Room 10, Bed A Upper deck.'),
(182, '2023-04-01 07:52:29.429999', '2023-04-01 07:52:29.429999', 1500.00, 'Vacant', 31, 'FM2FR10-BL', 'Female Dorm, 2nd Floor, Room 10, Bed B Lower deck.'),
(183, '2023-04-01 07:52:41.085470', '2023-04-01 07:52:41.085470', 1500.00, 'Vacant', 31, 'FM2FR10-CU', 'Female Dorm, 2nd Floor, Room 10, Bed C Upper deck.'),
(184, '2023-04-01 07:52:51.719902', '2023-04-01 07:52:51.719902', 1500.00, 'Vacant', 31, 'FM2FR10-DL', 'Female Dorm, 2nd Floor, Room 10, Bed D Lower deck.'),
(185, '2023-04-01 07:53:02.538787', '2023-04-01 07:53:02.538787', 1500.00, 'Vacant', 31, 'FM2FR10-EU', 'Female Dorm, 2nd Floor, Room 10, Bed E Upper deck.'),
(186, '2023-04-01 07:53:13.431645', '2023-04-01 07:53:13.431645', 1500.00, 'Vacant', 31, 'FM2FR10-FL', 'Female Dorm, 2nd Floor, Room 10, Bed F Lower deck.'),
(187, '2023-04-01 07:53:39.099689', '2023-04-01 07:53:39.099689', 1500.00, 'Vacant', 32, 'FM2FR11-AU', 'Female Dorm, 2nd Floor, Room 11, Bed A Upper deck.'),
(188, '2023-04-01 07:53:49.666008', '2023-04-01 07:53:49.666008', 1500.00, 'Vacant', 32, 'FM2FR11-BL', 'Female Dorm, 2nd Floor, Room 11, Bed B Lower deck.'),
(189, '2023-04-01 07:54:04.908330', '2023-04-01 07:54:04.908330', 1500.00, 'Vacant', 32, 'FM2FR11-CU', 'Female Dorm, 2nd Floor, Room 11, Bed C Upper deck.'),
(190, '2023-04-01 07:54:20.436495', '2023-04-01 07:54:20.436495', 1500.00, 'Vacant', 32, 'FM2FR11-DL', 'Female Dorm, 2nd Floor, Room 11, Bed D Lower deck.'),
(191, '2023-04-01 07:54:32.813064', '2023-04-01 07:54:32.813064', 1500.00, 'Vacant', 32, 'FM2FR11-EU', 'Female Dorm, 2nd Floor, Room 11, Bed E Upper deck.'),
(192, '2023-04-01 07:54:51.648738', '2023-04-01 07:54:51.648738', 1500.00, 'Vacant', 32, 'FM2FR11-FL', 'Female Dorm, 2nd Floor, Room 11, Bed F Lower deck.'),
(193, '2023-04-01 07:56:02.121952', '2023-04-01 07:56:02.121952', 1500.00, 'Vacant', 33, 'FM2FR12-AU', 'Female Dorm, 2nd Floor, Room 12, Bed A Upper deck.'),
(194, '2023-04-01 07:56:17.097678', '2023-04-01 07:56:17.097678', 1500.00, 'Vacant', 33, 'FM2FR12-BL', 'Female Dorm, 2nd Floor, Room 12, Bed B Lower deck.'),
(195, '2023-04-01 07:56:29.222980', '2023-04-01 07:56:29.222980', 1500.00, 'Vacant', 33, 'FM2FR12-CU', 'Female Dorm, 2nd Floor, Room 12, Bed C Upper deck.'),
(196, '2023-04-01 07:56:39.704859', '2023-04-01 07:56:39.704859', 1500.00, 'Vacant', 33, 'FM2FR12-DL', 'Female Dorm, 2nd Floor, Room 12, Bed D Lower deck.'),
(197, '2023-04-01 07:56:51.569225', '2023-04-01 07:56:51.569225', 1500.00, 'Vacant', 33, 'FM2FR12-EU', 'Female Dorm, 2nd Floor, Room 12, Bed E Upper deck.'),
(198, '2023-04-01 07:57:05.584786', '2023-04-01 07:57:05.584786', 1500.00, 'Vacant', 33, 'FM2FR12-FL', 'Female Dorm, 2nd Floor, Room 12, Bed F Lower deck.'),
(199, '2023-04-01 07:57:32.823903', '2023-04-01 07:57:32.823903', 1500.00, 'Vacant', 34, 'FM2FR13-AU', 'Female Dorm, 2nd Floor, Room 13, Bed A Upper deck.'),
(200, '2023-04-01 07:57:42.232230', '2023-04-01 07:57:42.232230', 1500.00, 'Vacant', 34, 'FM2FR13-BL', 'Female Dorm, 2nd Floor, Room 13, Bed B Lower deck.'),
(201, '2023-04-01 07:57:52.069781', '2023-04-01 07:57:52.072621', 1500.00, 'Vacant', 34, 'FM2FR13-CU', 'Female Dorm, 2nd Floor, Room 13, Bed C Upper deck.'),
(202, '2023-04-01 07:58:03.136504', '2023-04-01 07:58:03.138095', 1500.00, 'Vacant', 34, 'FM2FR13-DL', 'Female Dorm, 2nd Floor, Room 13, Bed D Lower deck.'),
(203, '2023-04-01 07:58:12.677304', '2023-04-01 07:58:12.677304', 1500.00, 'Vacant', 34, 'FM2FR13-EU', 'Female Dorm, 2nd Floor, Room 13, Bed E Upper deck.'),
(204, '2023-04-01 07:58:23.392061', '2023-04-01 07:58:23.392061', 1500.00, 'Vacant', 34, 'FM2FR13-FL', 'Female Dorm, 2nd Floor, Room 13, Bed F Lower deck.'),
(205, '2023-04-01 07:58:50.672188', '2023-04-01 07:58:50.672188', 1500.00, 'Vacant', 35, 'FM2FR14-AU', 'Female Dorm, 2nd Floor, Room 14, Bed A Upper deck.'),
(206, '2023-04-01 07:59:03.092508', '2023-04-01 07:59:03.092508', 1500.00, 'Vacant', 35, 'FM2FR14-BL', 'Female Dorm, 2nd Floor, Room 14, Bed B Lower deck.'),
(207, '2023-04-01 07:59:13.646227', '2023-04-01 07:59:13.646227', 1500.00, 'Vacant', 35, 'FM2FR14-CU', 'Female Dorm, 2nd Floor, Room 14, Bed C Upper deck.'),
(208, '2023-04-01 07:59:25.309398', '2023-04-01 07:59:25.309398', 1500.00, 'Vacant', 35, 'FM2FR14-DL', 'Female Dorm, 2nd Floor, Room 14, Bed D Lower deck.'),
(209, '2023-04-01 07:59:36.983001', '2023-04-01 07:59:36.983001', 1500.00, 'Vacant', 35, 'FM2FR14-EU', 'Female Dorm, 2nd Floor, Room 14, Bed E Upper deck.'),
(210, '2023-04-01 07:59:46.893430', '2023-04-01 07:59:46.893430', 1500.00, 'Vacant', 35, 'FM2FR14-FL', 'Female Dorm, 2nd Floor, Room 14, Bed F Lower deck.'),
(211, '2023-04-01 08:53:31.612356', '2023-04-01 08:53:31.612356', 1500.00, 'Vacant', 36, 'FM2FR15-AU', 'Female Dorm, 2nd Floor, Room 15, Bed A Upper deck.'),
(212, '2023-04-01 08:53:45.490639', '2023-04-01 08:53:45.490639', 1500.00, 'Vacant', 36, 'FM2FR15-BL', 'Female Dorm, 2nd Floor, Room 15, Bed B Lower deck.'),
(213, '2023-04-01 08:53:57.236951', '2023-04-01 08:53:57.236951', 1500.00, 'Vacant', 36, 'FM2FR15-CU', 'Female Dorm, 2nd Floor, Room 15, Bed C Upper deck.'),
(214, '2023-04-01 08:54:12.296335', '2023-04-01 08:54:12.296335', 1500.00, 'Vacant', 36, 'FM2FR15-DL', 'Female Dorm, 2nd Floor, Room 15, Bed D Lower deck.'),
(215, '2023-04-01 08:54:23.584334', '2023-04-01 08:54:23.584334', 1500.00, 'Vacant', 36, 'FM2FR15-EU', 'Female Dorm, 2nd Floor, Room 15, Bed E Upper deck.'),
(216, '2023-04-01 08:54:36.100179', '2023-04-01 08:54:36.100179', 1500.00, 'Vacant', 36, 'FM2FR15-FL', 'Female Dorm, 2nd Floor, Room 15, Bed F Lower deck.'),
(217, '2023-04-01 08:57:03.273515', '2023-04-01 08:57:03.273515', 1500.00, 'Vacant', 37, 'FM2FR16-AU', 'Female Dorm, 2nd Floor, Room 16, Bed A Upper deck.'),
(218, '2023-04-01 08:57:13.435763', '2023-04-01 08:57:13.435763', 1500.00, 'Vacant', 37, 'FM2FR16-BL', 'Female Dorm, 2nd Floor, Room 16, Bed B Lower deck.'),
(219, '2023-04-01 08:57:23.565589', '2023-04-01 08:57:23.565589', 1500.00, 'Vacant', 37, 'FM2FR16-CU', 'Female Dorm, 2nd Floor, Room 16, Bed C Upper deck.'),
(220, '2023-04-01 08:57:38.128289', '2023-04-01 08:57:38.128289', 1500.00, 'Vacant', 37, 'FM2FR16-DL', 'Female Dorm, 2nd Floor, Room 16, Bed D Lower deck.'),
(221, '2023-04-01 08:57:52.296464', '2023-04-01 08:57:52.296464', 1500.00, 'Vacant', 37, 'FM2FR16-EU', 'Female Dorm, 2nd Floor, Room 16, Bed E Upper deck.'),
(222, '2023-04-01 08:58:03.219321', '2023-04-01 08:58:03.219321', 1500.00, 'Vacant', 37, 'FM2FR16-FL', 'Female Dorm, 2nd Floor, Room 16, Bed F Lower deck.'),
(223, '2023-04-01 08:59:00.709491', '2023-04-01 08:59:00.709491', 1500.00, 'Vacant', 38, 'FM3FR17-AU', 'Female Dorm, 3rd Floor, Room 17, Bed A Upper deck.'),
(224, '2023-04-01 08:59:12.467336', '2023-04-01 08:59:12.467336', 1500.00, 'Vacant', 38, 'FM3FR17-BL', 'Female Dorm, 3rd Floor, Room 17, Bed B Lower deck.'),
(225, '2023-04-01 08:59:26.731599', '2023-04-01 08:59:26.731599', 1500.00, 'Vacant', 38, 'FM3FR17-CU', 'Female Dorm, 3rd Floor, Room 17, Bed C Upper deck.'),
(226, '2023-04-01 09:09:33.129376', '2023-04-01 09:09:33.129376', 1500.00, 'Vacant', 38, 'FM3FR17-DL', 'Female Dorm, 3rd Floor, Room 17, Bed D Lower deck.'),
(227, '2023-04-01 09:09:48.348781', '2023-04-01 09:09:48.348781', 1500.00, 'Vacant', 38, 'FM3FR17-EU', 'Female Dorm, 3rd Floor, Room 17, Bed E Upper deck.'),
(228, '2023-04-01 09:10:05.013164', '2023-04-01 09:10:05.013164', 1500.00, 'Vacant', 38, 'FM3FR17-FL', 'Female Dorm, 3rd Floor, Room 17, Bed F Lower deck.'),
(229, '2023-04-01 09:10:29.944780', '2023-04-01 09:10:29.944780', 1500.00, 'Vacant', 39, 'FM3FR18-AU', 'Female Dorm, 3rd Floor, Room 18, Bed A Upper deck.'),
(230, '2023-04-01 09:11:04.140517', '2023-04-01 09:11:04.140517', 1500.00, 'Vacant', 39, 'FM3FR18-BL', 'Female Dorm, 3rd Floor, Room 18, Bed B Lower deck.'),
(231, '2023-04-01 09:11:26.693361', '2023-04-01 09:11:26.693361', 1500.00, 'Vacant', 39, 'FM3FR18-CU', 'Female Dorm, 3rd Floor, Room 18, Bed C Upper deck.'),
(232, '2023-04-01 09:11:38.834149', '2023-04-01 09:11:38.834149', 1500.00, 'Vacant', 39, 'FM3FR18-DL', 'Female Dorm, 3rd Floor, Room 18, Bed D Lower deck.'),
(233, '2023-04-01 09:12:18.929953', '2023-04-01 09:12:18.929953', 1500.00, 'Vacant', 39, 'FM3FR18-EU', 'Female Dorm, 3rd Floor, Room 18, Bed E Upper deck.'),
(234, '2023-04-01 09:12:40.379455', '2023-04-01 09:12:40.379455', 1500.00, 'Vacant', 39, 'FM3FR18-FL', 'Female Dorm, 3rd Floor, Room 18, Bed F Lower deck.'),
(235, '2023-04-01 09:38:57.043152', '2023-04-01 09:38:57.043152', 1500.00, 'Vacant', 40, 'FM3FR19-AU', 'Female Dorm, 3rd Floor, Room 19, Bed A Upper deck.'),
(236, '2023-04-01 09:39:07.125685', '2023-04-01 09:39:07.125685', 1500.00, 'Vacant', 40, 'FM3FR19-BL', 'Female Dorm, 3rd Floor, Room 19, Bed B Lower deck.'),
(237, '2023-04-01 09:39:17.506398', '2023-04-01 09:39:17.506398', 1500.00, 'Vacant', 40, 'FM3FR19-CU', 'Female Dorm, 3rd Floor, Room 19, Bed C Upper deck.'),
(238, '2023-04-01 09:39:30.376696', '2023-04-01 09:39:30.377691', 1500.00, 'Vacant', 40, 'FM3FR19-DL', 'Female Dorm, 3rd Floor, Room 19, Bed D Lower deck.'),
(239, '2023-04-01 09:39:54.334934', '2023-04-01 09:39:54.334934', 1500.00, 'Vacant', 40, 'FM3FR19-EU', 'Female Dorm, 3rd Floor, Room 19, Bed E Upper deck.'),
(240, '2023-04-01 09:40:08.356419', '2023-04-01 09:40:08.356419', 1500.00, 'Vacant', 40, 'FM3FR19-FL', 'Female Dorm, 3rd Floor, Room 19, Bed F Lower deck.'),
(246, '2023-04-01 10:27:03.435527', '2023-04-01 10:27:03.435527', 1500.00, 'Vacant', 41, 'FM3FR20-AU', 'Female Dorm, 3rd Floor, Room 20, Bed A Upper deck.'),
(247, '2023-04-01 10:27:17.620613', '2023-04-01 10:27:17.620613', 1500.00, 'Vacant', 41, 'FM3FR20-BL', 'Female Dorm, 3rd Floor, Room 20, Bed B Lower deck.'),
(248, '2023-04-01 10:27:31.753252', '2023-04-01 10:27:31.753252', 1500.00, 'Vacant', 41, 'FM3FR20-CU', 'Female Dorm, 3rd Floor, Room 20, Bed C Upper deck.'),
(249, '2023-04-01 10:27:45.031535', '2023-04-01 10:27:45.031535', 1500.00, 'Vacant', 41, 'FM3FR20-DL', 'Female Dorm, 3rd Floor, Room 20, Bed D Lower deck.'),
(250, '2023-04-01 10:28:17.988681', '2023-04-01 10:28:17.988681', 1500.00, 'Vacant', 41, 'FM3FR20-EU', 'Female Dorm, 3rd Floor, Room 20, Bed E Upper deck.'),
(251, '2023-04-01 10:28:31.854019', '2023-04-01 10:28:31.854019', 1500.00, 'Vacant', 41, 'FM3FR20-FL', 'Female Dorm, 3rd Floor, Room 20, Bed F Lower deck.'),
(252, '2023-04-01 10:30:54.728732', '2023-04-01 10:30:54.728732', 1500.00, 'Vacant', 1, 'M1FR1-AU', 'Male Dorm, 1st Floor, Room 1, Bed A Upper deck.'),
(253, '2023-04-01 10:31:07.301346', '2023-04-01 10:31:07.301346', 1500.00, 'Vacant', 1, 'M1FR1-BL', 'Male Dorm, 1st Floor, Room 1, Bed B Lower deck.'),
(254, '2023-04-01 10:47:26.919637', '2023-04-01 10:47:26.919637', 1500.00, 'Vacant', 1, 'M1FR1-CU', 'Male Dorm, 1st Floor, Room 1, Bed C Upper deck.'),
(255, '2023-04-01 10:47:36.534076', '2023-04-01 10:47:36.534076', 1500.00, 'Vacant', 1, 'M1FR1-DL', 'Male Dorm, 1st Floor, Room 1, Bed D Lower deck.'),
(256, '2023-04-01 10:47:52.868875', '2023-04-01 10:47:52.868875', 1500.00, 'Vacant', 1, 'M1FR1-EU', 'Male Dorm, 1st Floor, Room 1, Bed E Upper deck.'),
(257, '2023-04-01 10:48:02.983414', '2023-04-01 10:48:02.983414', 1500.00, 'Vacant', 1, 'M1FR1-FL', 'Male Dorm, 1st Floor, Room 1, Bed F Lower deck.'),
(258, '2023-04-01 10:50:18.199593', '2023-04-01 10:50:18.199593', 1500.00, 'Vacant', 42, 'FM3FR21-AU', 'Female Dorm, 3rd Floor, Room 21, Bed A Upper deck.'),
(259, '2023-04-01 10:50:30.401132', '2023-04-01 10:50:30.401132', 1500.00, 'Vacant', 42, 'FM3FR21-BL', 'Female Dorm, 3rd Floor, Room 21, Bed B Lower deck.'),
(260, '2023-04-01 10:50:43.500855', '2023-04-01 10:50:43.500855', 1500.00, 'Vacant', 42, 'FM3FR21-CU', 'Female Dorm, 3rd Floor, Room 21, Bed C Upper deck.'),
(261, '2023-04-01 10:50:55.863557', '2023-04-01 10:50:55.863557', 1500.00, 'Vacant', 42, 'FM3FR21-DL', 'Female Dorm, 3rd Floor, Room 21, Bed D Lower deck.'),
(262, '2023-04-01 10:51:06.548218', '2023-04-01 10:51:06.548218', 1500.00, 'Vacant', 42, 'FM3FR21-EU', 'Female Dorm, 3rd Floor, Room 21, Bed E Upper deck.'),
(263, '2023-04-01 10:51:19.921156', '2023-04-01 10:51:19.922790', 1500.00, 'Vacant', 42, 'FM3FR21-FL', 'Female Dorm, 3rd Floor, Room 21, Bed F Lower deck.'),
(264, '2023-04-01 11:08:21.971684', '2023-04-01 11:08:21.971684', 1500.00, 'Vacant', 43, 'FM3FR22-AU', 'Female Dorm, 3rd Floor, Room 22, Bed A Upper deck.'),
(265, '2023-04-01 11:08:45.574136', '2023-04-01 11:08:45.574136', 1500.00, 'Vacant', 43, 'FM3FR22-BL', 'Female Dorm, 3rd Floor, Room 22, Bed B Lower deck.'),
(266, '2023-04-01 11:08:57.131639', '2023-04-01 11:08:57.131639', 1500.00, 'Vacant', 43, 'FM3FR22-CU', 'Female Dorm, 3rd Floor, Room 22, Bed C Upper deck.'),
(267, '2023-04-01 11:09:12.901977', '2023-04-01 11:09:12.901977', 1500.00, 'Vacant', 43, 'FM3FR22-DL', 'Female Dorm, 3rd Floor, Room 22, Bed D Lower deck.'),
(268, '2023-04-01 11:09:37.611288', '2023-04-01 11:09:37.611288', 1500.00, 'Vacant', 43, 'FM3FR22-EU', 'Female Dorm, 3rd Floor, Room 22, Bed E Upper deck.'),
(269, '2023-04-01 11:10:11.577884', '2023-04-01 11:10:11.577884', 1500.00, 'Vacant', 43, 'FM3FR22-FL', 'Female Dorm, 3rd Floor, Room 22, Bed F Lower deck.'),
(270, '2023-04-01 11:10:40.592570', '2023-04-01 11:10:40.592570', 1500.00, 'Vacant', 44, 'FM3FR23-AU', 'Female Dorm, 3rd Floor, Room 23, Bed A Upper deck.'),
(271, '2023-04-01 11:10:53.481828', '2023-04-01 11:10:53.481828', 1500.00, 'Vacant', 44, 'FM3FR23-BL', 'Female Dorm, 3rd Floor, Room 23, Bed B Lower deck.'),
(272, '2023-04-01 11:11:08.454143', '2023-04-01 11:11:08.454143', 1500.00, 'Vacant', 44, 'FM3FR23-CU', 'Female Dorm, 3rd Floor, Room 23, Bed C Upper deck.'),
(273, '2023-04-01 11:11:18.682960', '2023-04-01 11:11:18.682960', 1500.00, 'Vacant', 44, 'FM3FR23-DL', 'Female Dorm, 3rd Floor, Room 23, Bed D Lower deck.'),
(274, '2023-04-01 11:11:30.088000', '2023-04-01 11:11:30.088000', 1500.00, 'Vacant', 44, 'FM3FR23-EU', 'Female Dorm, 3rd Floor, Room 23, Bed E Upper deck.'),
(275, '2023-04-01 11:11:40.836844', '2023-04-01 11:11:40.836844', 1500.00, 'Vacant', 44, 'FM3FR23-FL', 'Female Dorm, 3rd Floor, Room 23, Bed F Lower deck.'),
(276, '2023-04-01 11:36:07.627577', '2023-04-01 11:36:07.627577', 1500.00, 'Vacant', 45, 'FM3FR24-AU', 'Female Dorm, 3rd Floor, Room 24, Bed A Upper deck.'),
(277, '2023-04-01 11:36:17.323384', '2023-04-01 11:36:17.323384', 1500.00, 'Vacant', 45, 'FM3FR24-BL', 'Female Dorm, 3rd Floor, Room 24, Bed B Lower deck.'),
(278, '2023-04-01 11:36:27.288158', '2023-04-01 11:36:27.288158', 1500.00, 'Vacant', 45, 'FM3FR24-CU', 'Female Dorm, 3rd Floor, Room 24, Bed  C Upper deck.'),
(279, '2023-04-01 11:36:37.215555', '2023-04-01 11:36:37.215555', 1500.00, 'Vacant', 45, 'FM3FR24-DL', 'Female Dorm, 3rd Floor, Room 24, Bed  D Lower deck.'),
(280, '2023-04-01 11:36:46.763372', '2023-04-01 11:36:46.763372', 1500.00, 'Vacant', 45, 'FM3FR24-EU', 'Female Dorm, 3rd Floor, Room 24, Bed  E Upper deck.'),
(281, '2023-04-01 11:36:58.518677', '2023-04-01 11:36:58.518677', 1500.00, 'Vacant', 45, 'FM3FR24-FL', 'Female Dorm, 3rd Floor, Room 24, Bed  F Lower deck.'),
(282, '2023-04-01 11:37:26.262639', '2023-04-01 11:37:26.262639', 1500.00, 'Vacant', 46, 'FM3FR25-AU', 'Female Dorm, 3rd Floor, Room 25, Bed A Upper deck.'),
(283, '2023-04-01 11:37:37.212720', '2023-04-01 11:37:37.212720', 1500.00, 'Vacant', 46, 'FM3FR25-BL', 'Female Dorm, 3rd Floor, Room 25, Bed B Lower deck.'),
(284, '2023-04-01 11:37:47.724497', '2023-04-01 11:37:47.724497', 1500.00, 'Vacant', 46, 'FM3FR25-CU', 'Female Dorm, 3rd Floor, Room 25, Bed C Upper deck.'),
(285, '2023-04-01 11:37:56.298109', '2023-04-01 11:37:56.298109', 1500.00, 'Vacant', 46, 'FM3FR25-DL', 'Female Dorm, 3rd Floor, Room 25, Bed D Lower deck.'),
(286, '2023-04-01 11:38:06.696520', '2023-04-01 11:38:06.696520', 1500.00, 'Vacant', 46, 'FM3FR25-EU', 'Female Dorm, 3rd Floor, Room 25, Bed E Upper deck.'),
(287, '2023-04-01 11:38:17.647286', '2023-04-01 11:38:17.647286', 1500.00, 'Vacant', 46, 'FM3FR25-FL', 'Female Dorm, 3rd Floor, Room 25, Bed F Lower deck.'),
(288, '2023-04-01 11:38:41.840788', '2023-04-01 11:38:41.840788', 1500.00, 'Vacant', 47, 'FM3FR26-AU', 'Female Dorm, 3rd Floor, Room 26, Bed A Upper deck.'),
(289, '2023-04-01 11:38:53.437628', '2023-04-01 11:38:53.437628', 1500.00, 'Vacant', 47, 'FM3FR26-BL', 'Female Dorm, 3rd Floor, Room 26, Bed B Lower deck.'),
(290, '2023-04-01 11:39:04.140725', '2023-04-01 11:39:04.140725', 1500.00, 'Vacant', 47, 'FM3FR26-CU', 'Female Dorm, 3rd Floor, Room 26, Bed C Upper deck.'),
(291, '2023-04-01 11:39:14.252953', '2023-04-01 11:39:14.252953', 1500.00, 'Vacant', 47, 'FM3FR26-DL', 'Female Dorm, 3rd Floor, Room 26, Bed D Lower deck.'),
(292, '2023-04-01 11:39:26.410082', '2023-04-01 11:39:26.410082', 1500.00, 'Vacant', 47, 'FM3FR26-EU', 'Female Dorm, 3rd Floor, Room 26, Bed E Upper deck.'),
(293, '2023-04-01 11:39:37.780654', '2023-04-01 11:39:37.780654', 1500.00, 'Vacant', 47, 'FM3FR26-FL', 'Female Dorm, 3rd Floor, Room 26, Bed F Lower deck.'),
(294, '2023-04-01 11:40:03.259643', '2023-04-01 11:40:03.259643', 1500.00, 'Vacant', 48, 'FM3FR27-AU', 'Female Dorm, 3rd Floor, Room 27, Bed A Upper deck.'),
(295, '2023-04-01 11:40:14.885263', '2023-04-01 11:40:14.885263', 1500.00, 'Vacant', 48, 'FM3FR27-BL', 'Female Dorm, 3rd Floor, Room 27, Bed B Lower deck.'),
(296, '2023-04-01 11:40:26.276146', '2023-04-01 11:40:26.276146', 1500.00, 'Vacant', 48, 'FM3FR27-CU', 'Female Dorm, 3rd Floor, Room 27, Bed C Upper deck.'),
(297, '2023-04-01 11:40:36.755318', '2023-04-01 11:40:36.755318', 1500.00, 'Vacant', 48, 'FM3FR27-DL', 'Female Dorm, 3rd Floor, Room 27, Bed D Lower deck.'),
(298, '2023-04-01 11:40:46.989335', '2023-04-01 11:40:46.989335', 1500.00, 'Vacant', 48, 'FM3FR27-EU', 'Female Dorm, 3rd Floor, Room 27, Bed E Upper deck.'),
(299, '2023-04-01 11:40:58.176365', '2023-04-01 11:40:58.176365', 1500.00, 'Vacant', 48, 'FM3FR27-FL', 'Female Dorm, 3rd Floor, Room 27, Bed F Lower deck.'),
(300, '2023-04-01 11:59:19.272926', '2023-04-01 11:59:19.272926', 4500.00, 'Vacant', 49, 'FR1FR1-A', 'Foreign Dorm, 1st Floor, Room 1, Bed A.'),
(301, '2023-04-01 11:59:31.251473', '2023-04-01 11:59:31.252488', 4500.00, 'Vacant', 49, 'FR1FR1-B', 'Foreign Dorm, 1st Floor, Room 1, Bed B.'),
(302, '2023-04-01 11:59:45.704749', '2023-04-01 11:59:45.704749', 4500.00, 'Vacant', 49, 'FR1FR1-C', 'Foreign Dorm, 1st Floor, Room 1, Bed C.'),
(303, '2023-04-01 12:01:08.563543', '2023-04-01 12:01:53.400123', 4500.00, 'Vacant', 50, 'FR1FR2-A', 'Foreign Dorm, 1st Floor, Room 2, Bed A.'),
(304, '2023-04-01 12:01:21.755090', '2023-04-01 12:02:01.008992', 4500.00, 'Vacant', 50, 'FR1FR2-B', 'Foreign Dorm, 1st Floor, Room 2, Bed B.'),
(305, '2023-04-01 12:01:37.015123', '2023-04-01 12:02:06.967958', 4500.00, 'Vacant', 50, 'FR1FR2-C', 'Foreign Dorm, 1st Floor, Room 2, Bed C.'),
(306, '2023-04-01 12:02:26.308549', '2023-04-01 12:02:38.174675', 4500.00, 'Vacant', 51, 'FR1FR3-A', 'Foreign Dorm, 1st Floor, Room 3, Bed A.'),
(307, '2023-04-01 12:03:02.310476', '2023-04-01 12:03:02.310476', 4500.00, 'Vacant', 51, 'FR1FR3-B', 'Foreign Dorm, 1st Floor, Room 3, Bed B.'),
(308, '2023-04-01 12:03:16.584937', '2023-04-01 12:03:16.584937', 4500.00, 'Vacant', 51, 'FR1FR3-C', 'Foreign Dorm, 1st Floor, Room 3, Bed C.'),
(309, '2023-04-01 12:03:43.331346', '2023-04-01 12:03:43.331346', 4500.00, 'Vacant', 52, 'FR2FR4-A', 'Foreign Dorm, 2nd Floor, Room 4, Bed A.'),
(310, '2023-04-01 12:03:56.296302', '2023-04-01 12:03:56.296302', 4500.00, 'Vacant', 52, 'FR2FR4-B', 'Foreign Dorm, 2nd Floor, Room 4, Bed B.'),
(311, '2023-04-01 12:04:11.363937', '2023-04-01 12:04:11.363937', 4500.00, 'Vacant', 52, 'FR2FR4-C', 'Foreign Dorm, 2nd Floor, Room 4, Bed C.'),
(312, '2023-04-01 12:06:28.857012', '2023-04-01 12:06:28.857012', 4500.00, 'Vacant', 53, 'FR2FR5-A', 'Foreign Dorm, 2nd Floor, Room 5, Bed A.'),
(313, '2023-04-01 12:06:44.155408', '2023-04-01 12:06:44.155408', 4500.00, 'Vacant', 53, 'FR2FR5-B', 'Foreign Dorm, 2nd Floor, Room 5, Bed B.'),
(314, '2023-04-01 12:06:57.950540', '2023-04-01 12:06:57.950540', 4500.00, 'Vacant', 53, 'FR2FR5-C', 'Foreign Dorm, 2nd Floor, Room 5, Bed C.'),
(315, '2023-04-01 12:07:41.616396', '2023-04-01 12:07:41.616396', 4500.00, 'Vacant', 54, 'FR2FR6-A', 'Foreign Dorm, 2nd Floor, Room 6, Bed A.'),
(316, '2023-04-01 12:07:55.064517', '2023-04-01 12:07:55.064517', 4500.00, 'Vacant', 54, 'FR2FR6-B', 'Foreign Dorm, 2nd Floor, Room 6, Bed B.'),
(317, '2023-04-01 12:08:08.384544', '2023-04-01 12:08:08.384544', 4500.00, 'Vacant', 54, 'FR2FR6-C', 'Foreign Dorm, 2nd Floor, Room 6, Bed C.'),
(318, '2023-04-01 12:08:38.505452', '2023-04-01 12:08:38.505452', 4500.00, 'Vacant', 55, 'FR2FR7-A', 'Foreign Dorm, 2nd Floor, Room 7, Bed A.'),
(319, '2023-04-01 12:08:59.008442', '2023-04-01 12:08:59.008442', 4500.00, 'Vacant', 55, 'FR2FR7-B', 'Foreign Dorm, 2nd Floor, Room 7, Bed B.'),
(320, '2023-04-01 12:09:17.147972', '2023-04-01 12:09:17.147972', 4500.00, 'Vacant', 55, 'FR2FR7-C', 'Foreign Dorm, 2nd Floor, Room 7, Bed C.'),
(321, '2023-04-01 12:10:09.747195', '2023-04-01 12:10:09.747195', 4500.00, 'Vacant', 56, 'FR2FR8-A', 'Foreign Dorm, 2nd Floor, Room 8, Bed A.'),
(322, '2023-04-01 12:10:23.121968', '2023-04-01 12:10:23.121968', 4500.00, 'Vacant', 56, 'FR2FR8-B', 'Foreign Dorm, 2nd Floor, Room 8, Bed B.'),
(323, '2023-04-01 12:10:34.141549', '2023-04-01 12:10:34.141549', 4500.00, 'Vacant', 56, 'FR2FR8-C', 'Foreign Dorm, 2nd Floor, Room 8, Bed C.'),
(324, '2023-04-01 12:10:53.709292', '2023-04-01 12:10:53.709292', 4500.00, 'Vacant', 57, 'FR2FR9-A', 'Foreign Dorm, 2nd Floor, Room 9, Bed A.'),
(325, '2023-04-01 12:11:05.080615', '2023-04-01 12:11:05.080615', 4500.00, 'Vacant', 57, 'FR2FR9-B', 'Foreign Dorm, 2nd Floor, Room 9, Bed B.'),
(326, '2023-04-01 12:11:17.374819', '2023-04-01 12:11:17.374819', 4500.00, 'Vacant', 57, 'FR2FR9-C', 'Foreign Dorm, 2nd Floor, Room 9, Bed C.'),
(327, '2023-04-01 12:11:40.239046', '2023-04-01 12:11:40.239046', 4500.00, 'Vacant', 58, 'FR2FR10-A', 'Foreign Dorm, 2nd Floor, Room 10, Bed A.'),
(328, '2023-04-01 12:11:52.412785', '2023-04-01 12:11:52.412785', 4500.00, 'Vacant', 58, 'FR2FR10-B', 'Foreign Dorm, 2nd Floor, Room 10, Bed B.'),
(329, '2023-04-01 12:12:04.937414', '2023-04-01 12:12:04.937414', 4500.00, 'Vacant', 58, 'FR2FR10-C', 'Foreign Dorm, 2nd Floor, Room 10, Bed C.'),
(330, '2023-04-01 12:12:30.782436', '2023-04-01 12:12:30.782436', 4500.00, 'Vacant', 59, 'FR2FR11-A', 'Foreign Dorm, 2nd Floor, Room 11, Bed A.'),
(331, '2023-04-01 12:12:46.167880', '2023-04-01 12:12:46.167880', 4500.00, 'Vacant', 59, 'FR2FR11-B', 'Foreign Dorm, 2nd Floor, Room 11, Bed B.'),
(332, '2023-04-01 12:12:59.206267', '2023-04-01 12:12:59.206267', 4500.00, 'Vacant', 59, 'FR2FR11-C', 'Foreign Dorm, 2nd Floor, Room 11, Bed C.'),
(333, '2023-04-01 12:13:23.765722', '2023-04-01 12:13:23.765722', 4500.00, 'Vacant', 60, 'FR2FR12-A', 'Foreign Dorm, 2nd Floor, Room 12, Bed A.'),
(334, '2023-04-01 12:13:33.535096', '2023-04-01 12:13:33.535096', 4500.00, 'Vacant', 60, 'FR2FR12-B', 'Foreign Dorm, 2nd Floor, Room 12, Bed B.'),
(335, '2023-04-01 12:13:46.208785', '2023-04-01 12:13:46.208785', 4500.00, 'Vacant', 60, 'FR2FR12-C', 'Foreign Dorm, 2nd Floor, Room 12, Bed C.'),
(336, '2023-04-01 12:14:12.434167', '2023-04-01 12:14:12.434167', 4500.00, 'Vacant', 61, 'FR2FR13-A', 'Foreign Dorm, 2nd Floor, Room 13, Bed A.'),
(337, '2023-04-01 12:14:22.552109', '2023-04-01 12:14:22.552109', 4500.00, 'Vacant', 61, 'FR2FR13-B', 'Foreign Dorm, 2nd Floor, Room 13, Bed B.'),
(338, '2023-04-01 12:14:33.059103', '2023-04-01 12:14:33.059103', 4500.00, 'Vacant', 61, 'FR2FR13-C', 'Foreign Dorm, 2nd Floor, Room 13, Bed C.');

-- --------------------------------------------------------

--
-- Table structure for table `dormitory_bedpricehistory`
--

CREATE TABLE `dormitory_bedpricehistory` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `start_date` datetime(6) DEFAULT NULL,
  `price` decimal(6,2) NOT NULL,
  `bed_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `dormitory_bill`
--

CREATE TABLE `dormitory_bill` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `bill_date` datetime(6) NOT NULL,
  `due_date` datetime(6) NOT NULL,
  `total` decimal(6,2) NOT NULL,
  `occupant_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `dormitory_bill_details`
--

CREATE TABLE `dormitory_bill_details` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `description` varchar(250) NOT NULL,
  `amount` decimal(6,2) DEFAULT NULL,
  `service_id` bigint(20) NOT NULL,
  `bill_date` datetime(6) NOT NULL,
  `occupant_id` bigint(20) DEFAULT NULL,
  `quantity` int(10) UNSIGNED NOT NULL
) ;

-- --------------------------------------------------------

--
-- Table structure for table `dormitory_demerit`
--

CREATE TABLE `dormitory_demerit` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `demerit_name` varchar(500) NOT NULL,
  `demerit_points` varchar(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `dormitory_demerit`
--

INSERT INTO `dormitory_demerit` (`id`, `created_at`, `updated_at`, `demerit_name`, `demerit_points`) VALUES
(1, '2023-04-15 14:51:48.191108', '2023-04-15 14:51:48.191108', 'Transfer to other rooms without permission', '5'),
(2, '2023-04-15 14:52:02.439630', '2023-04-15 14:52:02.440631', 'Doing malicious conduct on dormitory premises', '5'),
(3, '2023-04-15 14:53:04.610406', '2023-04-15 14:53:04.610406', 'Allowing opposite sex other than the parents to enter his/her room', '5'),
(4, '2023-04-15 14:53:10.520927', '2023-04-15 14:53:10.520927', 'Possessing inside the dormitory any firearm, bladed weapon, or any kind of dangerous and deadly weapon; Provided, that this shall not possess the in connection with their studies and have a permit for the purpose', '5'),
(5, '2023-04-15 14:53:19.111551', '2023-04-15 14:53:19.112550', 'Oral defamation against co-residents', '5'),
(6, '2023-04-15 14:53:27.151082', '2023-04-15 14:53:27.151082', 'Bullying', '5'),
(7, '2023-04-15 14:53:36.061604', '2023-04-15 14:53:36.061604', 'Threatening or any attempt to any member of the dormitory with physical harm; unlawfully preventing or threatening the dormitory residents or other dormitory officials to enter the dormitory premises', '5'),
(8, '2023-04-15 14:55:26.676819', '2023-04-15 14:55:26.676819', 'Non-Securing of Dormitory forms i.e. curfew extension and renewal/clearance forms', '4'),
(9, '2023-04-15 14:55:42.757115', '2023-04-15 14:55:42.757115', 'Non-Compliance related to room checking procedures', '4'),
(10, '2023-04-15 14:55:54.429380', '2023-04-15 14:55:54.429380', 'Non-Compliance to the administrative and dormitory superintendents', '4'),
(11, '2023-04-15 14:56:02.368974', '2023-04-15 14:56:02.368974', 'Bringing of appliances without the approval of the dormitory parent', '4'),
(12, '2023-04-15 15:09:13.746100', '2023-04-15 15:09:13.746100', 'Laundering of clothes inside the dormitory', '3'),
(13, '2023-04-15 15:09:22.017653', '2023-04-15 15:09:22.017653', 'Use electrical appliances, including ironing of clothes inside the dormitory', '3'),
(14, '2023-04-15 15:09:29.160302', '2023-04-15 15:09:29.160302', 'Returning after curfew hour or very late from time in indicated on the curfew extension form', '3'),
(15, '2023-04-15 15:09:37.841748', '2023-04-15 15:09:37.841748', 'Lending dormitory ID to the outsider and co-residents to enter the dormitory premises', '3'),
(16, '2023-04-15 15:09:58.399065', '2023-04-15 15:09:58.399065', 'Using other personal things without permission to the owner', '2'),
(17, '2023-04-15 15:10:13.010408', '2023-04-15 15:10:13.010408', 'Failure to do proper waste segregation and or throwing garbage in improper places', '2'),
(18, '2023-04-15 15:10:23.411027', '2023-04-15 15:10:23.411027', 'Disturbing / Disrespect on the privacy of others including making noise after curfew hours and playing loud music inside the dormitory', '2'),
(19, '2023-04-15 15:10:39.554984', '2023-04-15 15:10:39.554984', 'Vandalism', '2'),
(20, '2023-04-15 15:10:47.454010', '2023-04-15 15:10:47.454010', 'Failure to register in logbook', '1'),
(21, '2023-04-15 15:10:58.105923', '2023-04-15 15:10:58.105923', 'Not turning off the fan, aircon, lights and faucet', '1'),
(22, '2023-04-15 15:11:11.931081', '2023-04-15 15:11:11.931081', 'Shouting and making nuisance inside the dormitory', '1'),
(23, '2023-04-15 15:11:17.070820', '2023-04-15 15:11:17.070820', 'Bringing pets in the dormitory', '1'),
(24, '2023-04-15 15:11:23.082585', '2023-04-15 15:11:23.082585', 'Walking around beyond time limits (11:00 PM only)', '1');

-- --------------------------------------------------------

--
-- Table structure for table `dormitory_occupant`
--

CREATE TABLE `dormitory_occupant` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `start_date` datetime(6) DEFAULT NULL,
  `end_date` datetime(6) DEFAULT NULL,
  `bed_id` bigint(20) NOT NULL,
  `bedPrice` decimal(6,2) DEFAULT NULL,
  `person_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `dormitory_occupantdemerit`
--

CREATE TABLE `dormitory_occupantdemerit` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `cur_date` datetime(6) NOT NULL,
  `prev_remarks` longtext NOT NULL,
  `demerit_name_id` bigint(20) NOT NULL,
  `occupant_id` bigint(20) NOT NULL,
  `new_remarks` longtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `dormitory_payment`
--

CREATE TABLE `dormitory_payment` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `payment_date` datetime(6) DEFAULT NULL,
  `amount` decimal(6,2) NOT NULL,
  `receipt_no` varchar(250) NOT NULL,
  `occupant_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `dormitory_person`
--

CREATE TABLE `dormitory_person` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `office_dept` varchar(250) DEFAULT NULL,
  `program` varchar(250) NOT NULL,
  `gender` varchar(50) NOT NULL,
  `contact_no` varchar(128) NOT NULL,
  `address` varchar(250) NOT NULL,
  `city` varchar(250) NOT NULL,
  `country` varchar(250) NOT NULL,
  `municipality` varchar(250) NOT NULL,
  `province` varchar(250) NOT NULL,
  `psu_email` varchar(250) NOT NULL,
  `guardian_contact_no` varchar(128) NOT NULL,
  `guardian_email_address` varchar(250) NOT NULL,
  `guardian_first_name` varchar(250) NOT NULL,
  `guardian_last_name` varchar(250) NOT NULL,
  `guardian_present_address` varchar(250) NOT NULL,
  `first_name` varchar(250) NOT NULL,
  `last_name` varchar(250) NOT NULL,
  `middle_name` varchar(250) DEFAULT NULL,
  `boarder_type` varchar(50) NOT NULL,
  `Field1` tinyint(1) NOT NULL,
  `Field2` tinyint(1) NOT NULL,
  `Field3` tinyint(1) NOT NULL,
  `Field4` tinyint(1) NOT NULL,
  `Field5` tinyint(1) NOT NULL,
  `Field6` tinyint(1) NOT NULL,
  `Field7` tinyint(1) NOT NULL,
  `reg_status` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `dormitory_room`
--

CREATE TABLE `dormitory_room` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `room_name` varchar(25) NOT NULL,
  `floorlvl` varchar(25) NOT NULL,
  `dorm_name` varchar(25) NOT NULL,
  `description` longtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `dormitory_room`
--

INSERT INTO `dormitory_room` (`id`, `created_at`, `updated_at`, `room_name`, `floorlvl`, `dorm_name`, `description`) VALUES
(1, '2023-03-31 15:37:25.633354', '2023-04-16 05:09:07.313964', 'M1F-R1', '1', 'Male Dorm', 'Male Dorm, 1st Floor, Room 1.'),
(2, '2023-03-31 15:38:20.896392', '2023-03-31 15:38:20.896392', 'M1F-R2', '1', 'Male Dorm', 'Male Dorm, 1st Floor, Room 2.'),
(3, '2023-03-31 15:40:47.261193', '2023-04-15 15:34:54.248097', 'M1F-R3', '1', 'Male Dorm', 'Male Dorm, 1st Floor, Room 3.'),
(4, '2023-03-31 15:49:16.582974', '2023-03-31 15:49:16.582974', 'M1F-R4', '1', 'Male Dorm', 'Male Dorm, 1st Floor, Room 4.'),
(5, '2023-03-31 15:49:35.550420', '2023-03-31 15:49:35.550420', 'M1F-R5', '1', 'Male Dorm', 'Male Dorm, 1st Floor, Room 5.'),
(6, '2023-03-31 15:49:50.768460', '2023-03-31 15:49:50.768460', 'M1F-R6', '1', 'Male Dorm', 'Male Dorm, 1st Floor, Room 6.'),
(7, '2023-03-31 16:09:20.697603', '2023-03-31 16:09:20.697603', 'M1F-R7', '1', 'Male Dorm', 'Male Dorm, 1st Floor, Room 7.'),
(8, '2023-03-31 16:09:38.221510', '2023-03-31 16:09:38.221510', 'M1F-R8', '1', 'Male Dorm', 'Male Dorm, 1st Floor, Room 8.'),
(9, '2023-03-31 16:09:52.008183', '2023-03-31 16:09:52.008183', 'M1F-R9', '1', 'Male Dorm', 'Male Dorm, 1st Floor, Room 9.'),
(10, '2023-03-31 16:10:11.158874', '2023-03-31 16:10:11.158874', 'M1F-R10', '1', 'Male Dorm', 'Male Dorm, 1st Floor, Room 10.'),
(11, '2023-03-31 16:10:25.402732', '2023-03-31 16:10:25.402732', 'M2F-R11', '2', 'Male Dorm', 'Male Dorm, 2nd Floor, Room 11.'),
(12, '2023-03-31 16:10:37.848527', '2023-03-31 16:10:37.849527', 'M2F-R12', '2', 'Male Dorm', 'Male Dorm, 2nd Floor, Room 12.'),
(13, '2023-03-31 16:10:58.883432', '2023-03-31 16:10:58.883432', 'M2F-R13', '2', 'Male Dorm', 'Male Dorm, 2nd Floor, Room 13.'),
(14, '2023-03-31 16:11:12.489989', '2023-03-31 16:11:12.489989', 'M2F-R14', '2', 'Male Dorm', 'Male Dorm, 2nd Floor, Room 14.'),
(15, '2023-03-31 16:29:55.405911', '2023-03-31 16:29:55.405911', 'M2F-R15', '2', 'Male Dorm', 'Male Dorm, 2nd Floor, Room 15.'),
(16, '2023-03-31 16:30:38.784554', '2023-03-31 16:30:38.784554', 'M2F-R16', '2', 'Male Dorm', 'Male Dorm, 2nd Floor, Room 16.'),
(17, '2023-03-31 16:30:51.259890', '2023-03-31 16:30:51.259890', 'M2F-R17', '2', 'Male Dorm', 'Male Dorm, 2nd Floor, Room 17.'),
(18, '2023-03-31 16:31:03.802188', '2023-03-31 16:31:03.802188', 'M2F-R18', '2', 'Male Dorm', 'Male Dorm, 2nd Floor, Room 18.'),
(19, '2023-03-31 16:31:14.637423', '2023-03-31 16:31:14.637423', 'M2F-R19', '2', 'Male Dorm', 'Male Dorm, 2nd Floor, Room 19.'),
(20, '2023-03-31 16:31:25.507155', '2023-03-31 16:31:25.507155', 'M2F-R20', '2', 'Male Dorm', 'Male Dorm, 2nd Floor, Room 20.'),
(21, '2023-03-31 16:31:36.826019', '2023-03-31 16:31:36.826019', 'M2F-R21', '2', 'Male Dorm', 'Male Dorm, 2nd Floor, Room 21.'),
(22, '2023-03-31 16:46:43.789807', '2023-03-31 16:46:43.789807', 'FM1F-R1', '1', 'Female Dorm', 'Female Dorm, 1st Floor, Room 1.'),
(23, '2023-03-31 16:46:58.054740', '2023-03-31 16:46:58.054740', 'FM1F-R2', '1', 'Female Dorm', 'Female Dorm, 1st Floor, Room 2.'),
(24, '2023-03-31 16:47:10.667062', '2023-03-31 16:47:10.667062', 'FM1F-R3', '1', 'Female Dorm', 'Female Dorm, 1st Floor, Room 3.'),
(25, '2023-03-31 16:47:30.850065', '2023-03-31 16:47:30.850065', 'FM1F-R4', '1', 'Female Dorm', 'Female Dorm, 1st Floor, Room 4.'),
(26, '2023-03-31 16:47:45.665823', '2023-03-31 16:47:45.665823', 'FM1F-R5', '1', 'Female Dorm', 'Female Dorm, 1st Floor, Room 5.'),
(27, '2023-03-31 16:47:58.655822', '2023-03-31 16:47:58.655822', 'FM2F-R6', '2', 'Female Dorm', 'Female Dorm, 2nd Floor, Room 6.'),
(28, '2023-03-31 16:48:14.679232', '2023-03-31 16:48:14.679232', 'FM2F-R7', '2', 'Female Dorm', 'Female Dorm, 2nd Floor, Room 7.'),
(29, '2023-03-31 16:48:34.796215', '2023-03-31 16:48:34.796215', 'FM2F-R8', '2', 'Female Dorm', 'Female Dorm, 2nd Floor, Room 8.'),
(30, '2023-03-31 16:48:46.239617', '2023-03-31 16:48:46.239617', 'FM2F-R9', '2', 'Female Dorm', 'Female Dorm, 2nd Floor, Room 9.'),
(31, '2023-03-31 16:48:58.031452', '2023-03-31 16:48:58.031452', 'FM2F-R10', '2', 'Female Dorm', 'Female Dorm, 2nd Floor, Room 10.'),
(32, '2023-03-31 16:49:32.882459', '2023-03-31 16:49:32.882459', 'FM2F-R11', '2', 'Female Dorm', 'Female Dorm, 2nd Floor, Room 11.'),
(33, '2023-03-31 16:49:45.601196', '2023-03-31 16:49:45.601196', 'FM2F-R12', '2', 'Female Dorm', 'Female Dorm, 2nd Floor, Room 12.'),
(34, '2023-03-31 16:50:00.020277', '2023-03-31 16:50:00.020277', 'FM2F-R13', '2', 'Female Dorm', 'Female Dorm, 2nd Floor, Room 13.'),
(35, '2023-03-31 16:50:37.818074', '2023-03-31 16:50:37.818074', 'FM2F-R14', '2', 'Female Dorm', 'Female Dorm, 2nd Floor, Room 14.'),
(36, '2023-03-31 16:50:52.025819', '2023-03-31 16:50:52.025819', 'FM2F-R15', '2', 'Female Dorm', 'Female Dorm, 2nd Floor, Room 15.'),
(37, '2023-03-31 16:51:02.776426', '2023-03-31 16:51:02.776426', 'FM2F-R16', '2', 'Female Dorm', 'Female Dorm, 2nd Floor, Room 16.'),
(38, '2023-03-31 16:51:20.223028', '2023-03-31 16:51:20.223028', 'FM3F-R17', '3', 'Female Dorm', 'Female Dorm, 3rd Floor, Room 17.'),
(39, '2023-03-31 16:51:39.484477', '2023-03-31 16:51:39.484477', 'FM3F-R18', '3', 'Female Dorm', 'Female Dorm, 3rd Floor, Room 18.'),
(40, '2023-03-31 16:51:53.013133', '2023-03-31 16:51:53.013133', 'FM3F-R19', '3', 'Female Dorm', 'Female Dorm, 3rd Floor, Room 19.'),
(41, '2023-03-31 16:52:07.394534', '2023-03-31 16:52:07.394534', 'FM3F-R20', '3', 'Female Dorm', 'Female Dorm, 3rd Floor, Room 20.'),
(42, '2023-03-31 16:52:20.169322', '2023-03-31 16:52:20.169322', 'FM3F-R21', '3', 'Female Dorm', 'Female Dorm, 3rd Floor, Room 21.'),
(43, '2023-03-31 16:52:32.772045', '2023-03-31 16:52:32.772045', 'FM3F-R22', '3', 'Female Dorm', 'Female Dorm, 3rd Floor, Room 22.'),
(44, '2023-03-31 16:52:52.040881', '2023-03-31 16:52:52.040881', 'FM3F-R23', '3', 'Female Dorm', 'Female Dorm, 3rd Floor, Room 23.'),
(45, '2023-03-31 16:53:02.782074', '2023-03-31 16:53:02.782074', 'FM3F-R24', '3', 'Female Dorm', 'Female Dorm, 3rd Floor, Room 24.'),
(46, '2023-03-31 16:53:20.993646', '2023-03-31 16:53:20.993646', 'FM3F-R25', '3', 'Female Dorm', 'Female Dorm, 3rd Floor, Room 25.'),
(47, '2023-03-31 16:53:32.032770', '2023-03-31 16:53:32.032770', 'FM3F-R26', '3', 'Female Dorm', 'Female Dorm, 3rd Floor, Room 26.'),
(48, '2023-03-31 16:53:44.249752', '2023-03-31 16:53:44.249752', 'FM3F-R27', '3', 'Female Dorm', 'Female Dorm, 3rd Floor, Room 27.'),
(49, '2023-03-31 16:54:33.066065', '2023-03-31 16:54:33.066065', 'FR1F-R1', '1', 'Foreign Dorm', 'Foreign Dorm, 1st Floor, Room 1.'),
(50, '2023-03-31 16:54:53.750930', '2023-03-31 16:54:53.750930', 'FR1F-R2', '1', 'Foreign Dorm', 'Foreign Dorm, 1st Floor, Room 2.'),
(51, '2023-03-31 16:55:08.176648', '2023-03-31 16:55:08.176648', 'FR1F-R3', '1', 'Foreign Dorm', 'Foreign Dorm, 1st Floor, Room 3.'),
(52, '2023-03-31 16:55:25.641474', '2023-03-31 16:55:25.641474', 'FR2F-R4', '2', 'Foreign Dorm', 'Foreign Dorm, 2nd Floor, Room 4.'),
(53, '2023-03-31 16:55:55.500124', '2023-03-31 16:55:55.500124', 'FR2F-R5', '2', 'Foreign Dorm', 'Foreign Dorm, 2nd Floor, Room 5.'),
(54, '2023-03-31 16:56:05.597382', '2023-03-31 16:56:05.597382', 'FR2F-R6', '2', 'Foreign Dorm', 'Foreign Dorm, 2nd Floor, Room 6.'),
(55, '2023-03-31 16:56:23.776844', '2023-03-31 16:56:23.776844', 'FR2F-R7', '2', 'Foreign Dorm', 'Foreign Dorm, 2nd Floor, Room 7.'),
(56, '2023-03-31 16:56:33.342782', '2023-03-31 16:56:33.342782', 'FR2F-R8', '2', 'Foreign Dorm', 'Foreign Dorm, 2nd Floor, Room 8.'),
(57, '2023-03-31 16:56:48.507946', '2023-03-31 16:56:48.508952', 'FR2F-R9', '2', 'Foreign Dorm', 'Foreign Dorm, 2nd Floor, Room 9.'),
(58, '2023-03-31 16:56:59.296328', '2023-03-31 16:56:59.296328', 'FR2F-R10', '2', 'Foreign Dorm', 'Foreign Dorm, 2nd Floor, Room 10.'),
(59, '2023-03-31 16:57:12.822806', '2023-03-31 16:57:12.822806', 'FR2F-R11', '2', 'Foreign Dorm', 'Foreign Dorm, 2nd Floor, Room 11.'),
(60, '2023-03-31 16:57:53.580920', '2023-03-31 16:57:53.582230', 'FR2F-R12', '2', 'Foreign Dorm', 'Foreign Dorm, 2nd Floor, Room 12.'),
(61, '2023-03-31 16:58:27.025932', '2023-03-31 16:58:27.025932', 'FR2F-R13', '2', 'Foreign Dorm', 'Foreign Dorm, 2nd Floor, Room 13.');

-- --------------------------------------------------------

--
-- Table structure for table `dormitory_service`
--

CREATE TABLE `dormitory_service` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `service_name` varchar(100) NOT NULL,
  `base_amount` decimal(6,2) NOT NULL,
  `status` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `dormitory_service`
--

INSERT INTO `dormitory_service` (`id`, `created_at`, `updated_at`, `service_name`, `base_amount`, `status`) VALUES
(1, '2023-04-12 07:42:09.082477', '2023-04-12 07:42:09.082477', 'Local Deposit', 1500.00, 'Available'),
(2, '2023-04-12 07:42:20.751962', '2023-04-12 07:42:20.751962', 'Local Advance', 1500.00, 'Available'),
(3, '2023-04-12 07:42:32.115689', '2023-04-12 07:42:32.115689', 'Dorm ID', 150.00, 'Available'),
(4, '2023-04-12 07:42:42.919052', '2023-04-12 07:42:42.919052', 'Foreign Deposit', 4500.00, 'Available'),
(5, '2023-04-12 07:42:53.083990', '2023-04-12 07:42:53.083990', 'Foreign Advance', 4500.00, 'Available'),
(7, '2023-04-12 09:07:04.237910', '2023-04-12 09:07:04.237910', 'Breakfast', 100.00, 'Available'),
(8, '2023-04-12 18:10:43.813838', '2023-04-12 18:10:43.813838', 'Others', 0.00, 'Available'),
(9, '2023-04-15 15:50:51.917187', '2023-04-15 15:51:04.046198', 'Edited', 50.00, 'Available'),
(10, '2023-04-16 05:50:20.930590', '2023-04-16 06:05:01.246937', 'Sample', 30.00, 'Not Available');

-- --------------------------------------------------------

--
-- Table structure for table `dormitory_user`
--

CREATE TABLE `dormitory_user` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `lastname` varchar(100) NOT NULL,
  `firstname` varchar(100) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `security_question` varchar(250) DEFAULT NULL,
  `security_answer` varchar(250) DEFAULT NULL,
  `recovery_email` varchar(250) DEFAULT NULL,
  `user_status` varchar(20) DEFAULT NULL,
  `phone_number` varchar(20) NOT NULL,
  `person_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `dormitory_user`
--

INSERT INTO `dormitory_user` (`id`, `created_at`, `updated_at`, `lastname`, `firstname`, `username`, `password`, `security_question`, `security_answer`, `recovery_email`, `user_status`, `phone_number`, `person_id`) VALUES
(20, '2023-04-13 15:38:00.000000', '2023-04-16 18:34:56.146750', 'Recto', 'Queenie', '201980119@psu.palawan.edu.ph', '123456', 'In what city were you born?', 'Puerto', NULL, 'active', '+639685858588', 19),
(21, '2023-04-13 15:39:16.000000', '2023-04-13 15:39:16.000000', 'Velasco', 'Carl Kobe', '201980020@psu.palawan.edu.ph', '123456', '', '', '', 'active', '+639857474744', 20),
(22, '2023-04-13 15:40:40.000000', '2023-04-13 15:40:40.000000', 'Pascua', 'Shaira Gay', '201980098@psu.palawan.edu.ph', '123456', '', '', '', 'active', '+639636363666', 21),
(23, '2023-04-13 15:42:00.000000', '2023-04-13 15:42:00.000000', 'Martinez', 'Kristine Joy', 'kjmartinez@psu.palawan.edu.ph', '123456', '', '', '', 'active', '+639858585555', 22),
(24, '2023-04-13 15:57:44.000000', '2023-04-13 15:57:44.000000', 'Tabang', 'Christian', 'christiantabang@gmail.com', '123456', '', '', '', 'inactive', '+639857477777', 23),
(25, '2023-04-14 00:17:22.000000', '2023-04-14 00:17:22.000000', 'Escurel', 'Jhon Carlo', '20198120@psu.palawan.edu.ph', '123456', '', '', '', 'active', '+639856254144', 24),
(26, '2023-04-14 00:19:10.000000', '2023-04-14 00:19:10.000000', 'dssd', 'dssd', '201980120@psu.palawan.edu.ph', '123456', '', '', '', 'active', '+639685858888', 25),
(27, '2023-04-14 19:33:07.000000', '2023-04-15 16:17:03.688615', 'dada', 'dadda', '201980120@psu.palawan.edu.ph', '123456', NULL, NULL, NULL, 'active', '+639857858888', 26),
(28, '2023-04-15 20:04:19.000000', '2023-04-15 20:04:19.000000', 'Winchester', 'Dean', 'redpuddin417@gmail.com', '123456', '', '', '', 'active', '+639857474444', 27),
(29, '2023-04-16 02:03:27.000000', '2023-04-16 02:03:27.000000', 'ddd', 'dd', 'redpuddin417@gmail.com', '123456', '', '', '', 'active', '+639857477777', 28),
(30, '2023-04-16 02:10:18.000000', '2023-04-16 02:10:18.000000', 'dsdsd', 'dssd', 'redpuddin417@gmail.com', '123456', '', '', '', 'inactive', '+639858685588', 29);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `dormitory_admin`
--
ALTER TABLE `dormitory_admin`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dormitory_admin_created_at_9927de71` (`created_at`);

--
-- Indexes for table `dormitory_bed`
--
ALTER TABLE `dormitory_bed`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dormitory_bed_created_at_e1bfc593` (`created_at`),
  ADD KEY `dormitory_bed_room_id_0465b35d_fk` (`room_id`);

--
-- Indexes for table `dormitory_bedpricehistory`
--
ALTER TABLE `dormitory_bedpricehistory`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dormitory_bedpricehistory_created_at_fc9f9c7d` (`created_at`),
  ADD KEY `dormitory_bedpricehistory_bed_id_144816ed_fk` (`bed_id`);

--
-- Indexes for table `dormitory_bill`
--
ALTER TABLE `dormitory_bill`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dormitory_bill_created_at_e190f6b6` (`created_at`),
  ADD KEY `dormitory_bill_occupant_id_9d7a59cb_fk` (`occupant_id`);

--
-- Indexes for table `dormitory_bill_details`
--
ALTER TABLE `dormitory_bill_details`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dormitory_bill_details_created_at_d20f2466` (`created_at`),
  ADD KEY `dormitory_bill_details_service_id_025b45b1_fk` (`service_id`),
  ADD KEY `dormitory_bill_detai_occupant_id_479f61bc_fk_dormitory` (`occupant_id`);

--
-- Indexes for table `dormitory_demerit`
--
ALTER TABLE `dormitory_demerit`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dormitory_demerit_created_at_5417de28` (`created_at`);

--
-- Indexes for table `dormitory_occupant`
--
ALTER TABLE `dormitory_occupant`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dormitory_occupant_created_at_6a02d074` (`created_at`),
  ADD KEY `dormitory_occupant_bed_id_966338f2_fk` (`bed_id`),
  ADD KEY `dormitory_occupant_person_id_ec841a0a_fk` (`person_id`);

--
-- Indexes for table `dormitory_occupantdemerit`
--
ALTER TABLE `dormitory_occupantdemerit`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dormitory_occupant_demerit_created_at_549bf4c8` (`created_at`),
  ADD KEY `dormitory_occupantdemerit_demerit_name_id_c1bc890c_fk` (`demerit_name_id`),
  ADD KEY `dormitory_occupantdemerit_occupant_id_a0799a6d_fk` (`occupant_id`);

--
-- Indexes for table `dormitory_payment`
--
ALTER TABLE `dormitory_payment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dormitory_payment_created_at_9d1fc3be` (`created_at`),
  ADD KEY `dormitory_payment_occupant_id_5ef43b16_fk` (`occupant_id`);

--
-- Indexes for table `dormitory_person`
--
ALTER TABLE `dormitory_person`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dormitory_person_created_at_4958789e` (`created_at`);

--
-- Indexes for table `dormitory_room`
--
ALTER TABLE `dormitory_room`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dormitory_room_created_at_25d3cc38` (`created_at`);

--
-- Indexes for table `dormitory_service`
--
ALTER TABLE `dormitory_service`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dormitory_service_created_at_922e55d3` (`created_at`);

--
-- Indexes for table `dormitory_user`
--
ALTER TABLE `dormitory_user`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dormitory_user_created_at_c06c7f19` (`created_at`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=77;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=114;

--
-- AUTO_INCREMENT for table `dormitory_admin`
--
ALTER TABLE `dormitory_admin`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `dormitory_bed`
--
ALTER TABLE `dormitory_bed`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=341;

--
-- AUTO_INCREMENT for table `dormitory_bedpricehistory`
--
ALTER TABLE `dormitory_bedpricehistory`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `dormitory_bill`
--
ALTER TABLE `dormitory_bill`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `dormitory_bill_details`
--
ALTER TABLE `dormitory_bill_details`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `dormitory_demerit`
--
ALTER TABLE `dormitory_demerit`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `dormitory_occupant`
--
ALTER TABLE `dormitory_occupant`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `dormitory_occupantdemerit`
--
ALTER TABLE `dormitory_occupantdemerit`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `dormitory_payment`
--
ALTER TABLE `dormitory_payment`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `dormitory_person`
--
ALTER TABLE `dormitory_person`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table `dormitory_room`
--
ALTER TABLE `dormitory_room`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=65;

--
-- AUTO_INCREMENT for table `dormitory_service`
--
ALTER TABLE `dormitory_service`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `dormitory_user`
--
ALTER TABLE `dormitory_user`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `dormitory_bed`
--
ALTER TABLE `dormitory_bed`
  ADD CONSTRAINT `dormitory_bed_room_id_0465b35d_fk` FOREIGN KEY (`room_id`) REFERENCES `dormitory_room` (`id`);

--
-- Constraints for table `dormitory_bedpricehistory`
--
ALTER TABLE `dormitory_bedpricehistory`
  ADD CONSTRAINT `dormitory_bedpricehistory_bed_id_144816ed_fk` FOREIGN KEY (`bed_id`) REFERENCES `dormitory_bed` (`id`);

--
-- Constraints for table `dormitory_bill`
--
ALTER TABLE `dormitory_bill`
  ADD CONSTRAINT `dormitory_bill_occupant_id_9d7a59cb_fk` FOREIGN KEY (`occupant_id`) REFERENCES `dormitory_occupant` (`id`);

--
-- Constraints for table `dormitory_bill_details`
--
ALTER TABLE `dormitory_bill_details`
  ADD CONSTRAINT `dormitory_bill_detai_occupant_id_479f61bc_fk_dormitory` FOREIGN KEY (`occupant_id`) REFERENCES `dormitory_occupant` (`id`),
  ADD CONSTRAINT `dormitory_bill_details_service_id_025b45b1_fk` FOREIGN KEY (`service_id`) REFERENCES `dormitory_service` (`id`);

--
-- Constraints for table `dormitory_occupant`
--
ALTER TABLE `dormitory_occupant`
  ADD CONSTRAINT `dormitory_occupant_bed_id_966338f2_fk` FOREIGN KEY (`bed_id`) REFERENCES `dormitory_bed` (`id`),
  ADD CONSTRAINT `dormitory_occupant_person_id_ec841a0a_fk` FOREIGN KEY (`person_id`) REFERENCES `dormitory_person` (`id`);

--
-- Constraints for table `dormitory_occupantdemerit`
--
ALTER TABLE `dormitory_occupantdemerit`
  ADD CONSTRAINT `dormitory_occupantdemerit_demerit_name_id_c1bc890c_fk` FOREIGN KEY (`demerit_name_id`) REFERENCES `dormitory_demerit` (`id`),
  ADD CONSTRAINT `dormitory_occupantdemerit_occupant_id_a0799a6d_fk` FOREIGN KEY (`occupant_id`) REFERENCES `dormitory_occupant` (`id`);

--
-- Constraints for table `dormitory_payment`
--
ALTER TABLE `dormitory_payment`
  ADD CONSTRAINT `dormitory_payment_occupant_id_5ef43b16_fk` FOREIGN KEY (`occupant_id`) REFERENCES `dormitory_occupant` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
