-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 23, 2025 at 12:43 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `verifikasi_tugas`
--

-- --------------------------------------------------------

--
-- Table structure for table `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('aae8492597af');

-- --------------------------------------------------------

--
-- Table structure for table `assignments`
--

CREATE TABLE `assignments` (
  `assignment_id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `image_path` varchar(255) NOT NULL,
  `submission_date` date DEFAULT NULL,
  `status` enum('PENDING','COCOK','TIDAK_COCOK') DEFAULT NULL,
  `verified_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `assignments`
--

INSERT INTO `assignments` (`assignment_id`, `student_id`, `image_path`, `submission_date`, `status`, `verified_at`) VALUES
(31, 7, 'static/uploads/assignments/assignment7_20250408115740.png', '2025-04-08', 'COCOK', '2025-04-08 04:57:46'),
(32, 7, 'static/uploads/assignments/assignment7_20250408123528.png', '2025-04-08', 'TIDAK_COCOK', '2025-04-08 20:10:05'),
(33, 5, 'static/uploads/assignments/assignment5_20250409030906.png', '2025-04-08', 'PENDING', NULL),
(34, 8, 'static/uploads/assignments/assignment8_20250412040007.png', '2025-04-11', 'PENDING', NULL),
(36, 14, 'static/uploads/assignments/assignment14_20250417021749.jpg', '2025-04-16', 'COCOK', '2025-04-16 19:17:59'),
(37, 14, 'static/uploads/assignments/assignment14_20250417021922.jpg', '2025-04-16', 'COCOK', '2025-04-16 19:19:30'),
(38, 14, 'static/uploads/assignments/assignment14_20250417022021.jpg', '2025-04-16', 'TIDAK_COCOK', '2025-04-16 19:20:29'),
(39, 14, 'static/uploads/assignments/assignment14_20250417022100.png', '2025-04-16', 'COCOK', '2025-04-16 19:21:08'),
(40, 14, 'static/uploads/assignments/assignment14_20250417024420.png', '2025-04-16', 'COCOK', '2025-04-16 19:44:27'),
(41, 14, 'static/uploads/assignments/assignment14_20250418062839.jpg', '2025-04-17', 'TIDAK_COCOK', '2025-04-17 23:28:58'),
(42, 14, 'static/uploads/assignments/assignment14_20250418063020.jpg', '2025-04-17', 'TIDAK_COCOK', '2025-04-17 23:30:32'),
(43, 14, 'static/uploads/assignments/assignment14_20250419123700.jpg', '2025-04-19', 'COCOK', '2025-04-19 05:41:31'),
(45, 14, 'static/uploads/assignments/assignment14_20250419124225.png', '2025-04-19', 'TIDAK_COCOK', '2025-04-19 05:42:32');

-- --------------------------------------------------------

--
-- Table structure for table `handwriting_samples`
--

CREATE TABLE `handwriting_samples` (
  `sample_id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `image_path` varchar(255) NOT NULL,
  `uploaded_at` datetime DEFAULT NULL,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `handwriting_samples`
--

INSERT INTO `handwriting_samples` (`sample_id`, `student_id`, `image_path`, `uploaded_at`, `description`) VALUES
(16, 7, 'static/uploads/handwriting_samples/sample7_20250407222823.png', '2025-04-07 15:28:23', 'Sample1'),
(17, 7, 'static/uploads/handwriting_samples/sample7_20250407222848.png', '2025-04-07 15:28:48', 'Sample2'),
(18, 7, 'static/uploads/handwriting_samples/sample7_20250407222902.png', '2025-04-07 15:29:02', 'Sample3'),
(19, 7, 'static/uploads/handwriting_samples/sample7_20250407222917.png', '2025-04-07 15:29:17', 'Sample4'),
(20, 7, 'static/uploads/handwriting_samples/sample7_20250407222932.png', '2025-04-07 15:29:32', 'Sample5'),
(21, 7, 'static/uploads/handwriting_samples/sample7_20250407222944.png', '2025-04-07 15:29:44', 'Sample6'),
(22, 7, 'static/uploads/handwriting_samples/sample7_20250407222954.png', '2025-04-07 15:29:54', 'Sample7'),
(23, 7, 'static/uploads/handwriting_samples/sample7_20250407223014.png', '2025-04-07 15:30:14', 'Sample8'),
(24, 7, 'static/uploads/handwriting_samples/sample7_20250407223025.png', '2025-04-07 15:30:25', 'Sample9'),
(25, 7, 'static/uploads/handwriting_samples/sample7_20250407223034.png', '2025-04-07 15:30:34', 'Sample10'),
(27, 14, 'static/uploads/handwriting_samples/sample14_20250416233929.jpg', '2025-04-16 16:39:29', ''),
(28, 14, 'static/uploads/handwriting_samples/sample14_20250416234204.jpg', '2025-04-16 16:42:04', ''),
(29, 14, 'static/uploads/handwriting_samples/sample14_20250416234211.jpg', '2025-04-16 16:42:11', ''),
(30, 14, 'static/uploads/handwriting_samples/sample14_20250416234224.jpg', '2025-04-16 16:42:24', ''),
(31, 14, 'static/uploads/handwriting_samples/sample14_20250416234231.jpg', '2025-04-16 16:42:31', ''),
(32, 14, 'static/uploads/handwriting_samples/sample14_20250416234238.jpg', '2025-04-16 16:42:38', ''),
(33, 14, 'static/uploads/handwriting_samples/sample14_20250416234253.jpg', '2025-04-16 16:42:53', ''),
(34, 14, 'static/uploads/handwriting_samples/sample14_20250416234301.jpg', '2025-04-16 16:43:01', ''),
(35, 14, 'static/uploads/handwriting_samples/sample14_20250416234307.jpg', '2025-04-16 16:43:07', ''),
(36, 14, 'static/uploads/handwriting_samples/sample14_20250416234316.jpg', '2025-04-16 16:43:16', ''),
(37, 14, 'static/uploads/handwriting_samples/sample14_20250416234322.jpg', '2025-04-16 16:43:22', ''),
(38, 14, 'static/uploads/handwriting_samples/sample14_20250416234328.jpg', '2025-04-16 16:43:28', ''),
(39, 14, 'static/uploads/handwriting_samples/sample14_20250416234334.jpg', '2025-04-16 16:43:34', ''),
(40, 14, 'static/uploads/handwriting_samples/sample14_20250416234411.jpg', '2025-04-16 16:44:11', ''),
(41, 14, 'static/uploads/handwriting_samples/sample14_20250416234424.jpg', '2025-04-16 16:44:24', ''),
(42, 14, 'static/uploads/handwriting_samples/sample14_20250416234430.jpg', '2025-04-16 16:44:30', ''),
(43, 14, 'static/uploads/handwriting_samples/sample14_20250416234437.jpg', '2025-04-16 16:44:37', ''),
(44, 14, 'static/uploads/handwriting_samples/sample14_20250416234443.jpg', '2025-04-16 16:44:43', ''),
(45, 14, 'static/uploads/handwriting_samples/sample14_20250416234453.jpg', '2025-04-16 16:44:53', ''),
(46, 14, 'static/uploads/handwriting_samples/sample14_20250416234502.jpg', '2025-04-16 16:45:02', ''),
(47, 14, 'static/uploads/handwriting_samples/sample14_20250416234514.jpg', '2025-04-16 16:45:14', ''),
(48, 14, 'static/uploads/handwriting_samples/sample14_20250416234523.jpg', '2025-04-16 16:45:23', ''),
(49, 14, 'static/uploads/handwriting_samples/sample14_20250416234529.jpg', '2025-04-16 16:45:29', ''),
(50, 14, 'static/uploads/handwriting_samples/sample14_20250416234537.jpg', '2025-04-16 16:45:37', ''),
(51, 14, 'static/uploads/handwriting_samples/sample14_20250416234543.jpg', '2025-04-16 16:45:43', ''),
(52, 5, 'static/uploads/handwriting_samples/sample5_20250417145052.png', '2025-04-17 07:50:52', ''),
(53, 5, 'static/uploads/handwriting_samples/sample5_20250417145100.png', '2025-04-17 07:51:00', ''),
(54, 5, 'static/uploads/handwriting_samples/sample5_20250417145107.png', '2025-04-17 07:51:07', ''),
(55, 5, 'static/uploads/handwriting_samples/sample5_20250417145114.png', '2025-04-17 07:51:14', ''),
(56, 5, 'static/uploads/handwriting_samples/sample5_20250417145128.png', '2025-04-17 07:51:28', ''),
(57, 5, 'static/uploads/handwriting_samples/sample5_20250417145140.png', '2025-04-17 07:51:40', ''),
(58, 5, 'static/uploads/handwriting_samples/sample5_20250417145147.png', '2025-04-17 07:51:47', ''),
(59, 5, 'static/uploads/handwriting_samples/sample5_20250417145156.png', '2025-04-17 07:51:56', ''),
(60, 5, 'static/uploads/handwriting_samples/sample5_20250417145203.png', '2025-04-17 07:52:03', ''),
(61, 5, 'static/uploads/handwriting_samples/sample5_20250417145210.png', '2025-04-17 07:52:10', ''),
(62, 6, 'static/uploads/handwriting_samples/sample6_20250417150009.png', '2025-04-17 08:00:09', ''),
(63, 6, 'static/uploads/handwriting_samples/sample6_20250417150017.png', '2025-04-17 08:00:17', ''),
(64, 6, 'static/uploads/handwriting_samples/sample6_20250417150023.png', '2025-04-17 08:00:23', ''),
(65, 6, 'static/uploads/handwriting_samples/sample6_20250417150029.png', '2025-04-17 08:00:29', ''),
(66, 6, 'static/uploads/handwriting_samples/sample6_20250417150037.png', '2025-04-17 08:00:37', ''),
(67, 6, 'static/uploads/handwriting_samples/sample6_20250417150048.png', '2025-04-17 08:00:48', ''),
(68, 6, 'static/uploads/handwriting_samples/sample6_20250417150103.png', '2025-04-17 08:01:03', ''),
(69, 6, 'static/uploads/handwriting_samples/sample6_20250417150111.png', '2025-04-17 08:01:11', ''),
(70, 6, 'static/uploads/handwriting_samples/sample6_20250417150116.png', '2025-04-17 08:01:16', ''),
(71, 6, 'static/uploads/handwriting_samples/sample6_20250417150121.png', '2025-04-17 08:01:21', ''),
(72, 8, 'static/uploads/handwriting_samples/sample8_20250417150226.png', '2025-04-17 08:02:26', ''),
(73, 8, 'static/uploads/handwriting_samples/sample8_20250417150233.png', '2025-04-17 08:02:33', ''),
(74, 8, 'static/uploads/handwriting_samples/sample8_20250417150241.png', '2025-04-17 08:02:41', ''),
(75, 8, 'static/uploads/handwriting_samples/sample8_20250417150247.png', '2025-04-17 08:02:47', ''),
(76, 8, 'static/uploads/handwriting_samples/sample8_20250417150254.png', '2025-04-17 08:02:54', ''),
(77, 8, 'static/uploads/handwriting_samples/sample8_20250417150300.png', '2025-04-17 08:03:00', ''),
(78, 8, 'static/uploads/handwriting_samples/sample8_20250417150306.png', '2025-04-17 08:03:06', ''),
(79, 8, 'static/uploads/handwriting_samples/sample8_20250417150312.png', '2025-04-17 08:03:12', ''),
(80, 8, 'static/uploads/handwriting_samples/sample8_20250417150413.png', '2025-04-17 08:04:13', ''),
(81, 8, 'static/uploads/handwriting_samples/sample8_20250417150419.png', '2025-04-17 08:04:19', ''),
(82, 9, 'static/uploads/handwriting_samples/sample9_20250417150431.png', '2025-04-17 08:04:31', ''),
(83, 9, 'static/uploads/handwriting_samples/sample9_20250417150439.png', '2025-04-17 08:04:39', ''),
(84, 9, 'static/uploads/handwriting_samples/sample9_20250417150447.png', '2025-04-17 08:04:47', ''),
(85, 9, 'static/uploads/handwriting_samples/sample9_20250417150454.png', '2025-04-17 08:04:54', ''),
(86, 9, 'static/uploads/handwriting_samples/sample9_20250417150615.png', '2025-04-17 08:06:15', ''),
(87, 9, 'static/uploads/handwriting_samples/sample9_20250417150833.png', '2025-04-17 08:08:33', ''),
(88, 9, 'static/uploads/handwriting_samples/sample9_20250417150841.png', '2025-04-17 08:08:41', ''),
(89, 9, 'static/uploads/handwriting_samples/sample9_20250417151153.png', '2025-04-17 08:11:53', ''),
(90, 9, 'static/uploads/handwriting_samples/sample9_20250417151205.png', '2025-04-17 08:12:05', ''),
(94, 9, 'static/uploads/handwriting_samples/sample9_20250417151319.png', '2025-04-17 08:13:19', ''),
(95, 10, 'static/uploads/handwriting_samples/sample10_20250417151623.jpg', '2025-04-17 08:16:23', ''),
(96, 10, 'static/uploads/handwriting_samples/sample10_20250417151632.jpg', '2025-04-17 08:16:32', ''),
(97, 10, 'static/uploads/handwriting_samples/sample10_20250417151641.jpg', '2025-04-17 08:16:41', ''),
(98, 10, 'static/uploads/handwriting_samples/sample10_20250417153117876117.jpg', '2025-04-17 08:31:17', ''),
(99, 10, 'static/uploads/handwriting_samples/sample10_20250417153117879117.jpg', '2025-04-17 08:31:17', ''),
(100, 10, 'static/uploads/handwriting_samples/sample10_20250417153117883120.jpg', '2025-04-17 08:31:17', ''),
(101, 10, 'static/uploads/handwriting_samples/sample10_20250417153117886118.jpg', '2025-04-17 08:31:17', ''),
(102, 10, 'static/uploads/handwriting_samples/sample10_20250417153133878323.jpg', '2025-04-17 08:31:33', ''),
(103, 10, 'static/uploads/handwriting_samples/sample10_20250417153133882326.jpg', '2025-04-17 08:31:34', ''),
(104, 10, 'static/uploads/handwriting_samples/sample10_20250417153133886325.jpg', '2025-04-17 08:31:34', ''),
(105, 10, 'static/uploads/handwriting_samples/sample10_20250417153133890324.jpg', '2025-04-17 08:31:34', ''),
(106, 10, 'static/uploads/handwriting_samples/sample10_20250417153133892325.jpg', '2025-04-17 08:31:34', ''),
(107, 10, 'static/uploads/handwriting_samples/sample10_20250417153133896325.jpg', '2025-04-17 08:31:34', ''),
(108, 10, 'static/uploads/handwriting_samples/sample10_20250417153133901327.jpg', '2025-04-17 08:31:34', ''),
(109, 10, 'static/uploads/handwriting_samples/sample10_20250417153133905326.jpg', '2025-04-17 08:31:34', ''),
(110, 10, 'static/uploads/handwriting_samples/sample10_20250417153133921325.jpg', '2025-04-17 08:31:34', ''),
(111, 10, 'static/uploads/handwriting_samples/sample10_20250417153133926325.jpg', '2025-04-17 08:31:34', ''),
(112, 10, 'static/uploads/handwriting_samples/sample10_20250417153133930324.jpg', '2025-04-17 08:31:34', ''),
(113, 10, 'static/uploads/handwriting_samples/sample10_20250417153133956324.jpg', '2025-04-17 08:31:34', ''),
(114, 10, 'static/uploads/handwriting_samples/sample10_20250417153133962327.jpg', '2025-04-17 08:31:34', ''),
(115, 10, 'static/uploads/handwriting_samples/sample10_20250417153133968325.jpg', '2025-04-17 08:31:34', ''),
(116, 10, 'static/uploads/handwriting_samples/sample10_20250417153133972325.jpg', '2025-04-17 08:31:34', ''),
(117, 10, 'static/uploads/handwriting_samples/sample10_20250417153133975325.jpg', '2025-04-17 08:31:34', ''),
(118, 10, 'static/uploads/handwriting_samples/sample10_20250417153133987762.jpg', '2025-04-17 08:31:34', ''),
(119, 10, 'static/uploads/handwriting_samples/sample10_20250417153133990762.jpg', '2025-04-17 08:31:34', ''),
(120, 15, 'static/uploads/handwriting_samples/sample15_20250417153210642748.jpg', '2025-04-17 08:32:10', ''),
(121, 15, 'static/uploads/handwriting_samples/sample15_20250417153210645746.jpg', '2025-04-17 08:32:10', ''),
(122, 15, 'static/uploads/handwriting_samples/sample15_20250417153210648747.jpg', '2025-04-17 08:32:10', ''),
(123, 15, 'static/uploads/handwriting_samples/sample15_20250417153210654746.jpg', '2025-04-17 08:32:10', ''),
(124, 15, 'static/uploads/handwriting_samples/sample15_20250417153210658745.jpg', '2025-04-17 08:32:10', ''),
(125, 15, 'static/uploads/handwriting_samples/sample15_20250417153210662746.jpg', '2025-04-17 08:32:10', ''),
(126, 15, 'static/uploads/handwriting_samples/sample15_20250417153210667746.jpg', '2025-04-17 08:32:10', ''),
(127, 15, 'static/uploads/handwriting_samples/sample15_20250417153210672746.jpg', '2025-04-17 08:32:10', ''),
(128, 15, 'static/uploads/handwriting_samples/sample15_20250417153210675746.jpg', '2025-04-17 08:32:10', ''),
(129, 15, 'static/uploads/handwriting_samples/sample15_20250417153210680751.jpg', '2025-04-17 08:32:10', ''),
(130, 15, 'static/uploads/handwriting_samples/sample15_20250417153210683746.jpg', '2025-04-17 08:32:10', ''),
(131, 15, 'static/uploads/handwriting_samples/sample15_20250417153210686746.jpg', '2025-04-17 08:32:10', ''),
(132, 15, 'static/uploads/handwriting_samples/sample15_20250417153210690746.jpg', '2025-04-17 08:32:10', ''),
(133, 15, 'static/uploads/handwriting_samples/sample15_20250417153210693750.jpg', '2025-04-17 08:32:10', ''),
(134, 15, 'static/uploads/handwriting_samples/sample15_20250417153210698747.jpg', '2025-04-17 08:32:10', ''),
(135, 15, 'static/uploads/handwriting_samples/sample15_20250417153210712749.jpg', '2025-04-17 08:32:10', ''),
(136, 15, 'static/uploads/handwriting_samples/sample15_20250417153210718746.jpg', '2025-04-17 08:32:10', ''),
(137, 15, 'static/uploads/handwriting_samples/sample15_20250417153210723746.jpg', '2025-04-17 08:32:10', ''),
(138, 15, 'static/uploads/handwriting_samples/sample15_20250417153210728746.jpg', '2025-04-17 08:32:10', ''),
(139, 15, 'static/uploads/handwriting_samples/sample15_20250417153210736747.jpg', '2025-04-17 08:32:10', ''),
(140, 15, 'static/uploads/handwriting_samples/sample15_20250417153210740746.jpg', '2025-04-17 08:32:10', ''),
(141, 15, 'static/uploads/handwriting_samples/sample15_20250417153210747747.jpg', '2025-04-17 08:32:10', ''),
(142, 15, 'static/uploads/handwriting_samples/sample15_20250417153210752747.jpg', '2025-04-17 08:32:10', ''),
(143, 15, 'static/uploads/handwriting_samples/sample15_20250417153210758746.jpg', '2025-04-17 08:32:10', ''),
(144, 15, 'static/uploads/handwriting_samples/sample15_20250417153210763747.jpg', '2025-04-17 08:32:10', '');

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `notification_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `message` text NOT NULL,
  `status` enum('UNREAD','READ') DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `notifications`
--

INSERT INTO `notifications` (`notification_id`, `user_id`, `message`, `status`, `created_at`) VALUES
(1, 1, 'Tugas siswa telah diverifikasi', 'READ', NULL),
(2, 1, 'Siswa baru telah ditambahkan', 'READ', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `student_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `class_name` varchar(50) NOT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`student_id`, `name`, `class_name`, `created_at`) VALUES
(5, 'Al-Faro', '6A', '2025-03-16 09:51:44'),
(6, 'Aulia', '6A', '2025-03-16 09:51:53'),
(7, 'Azizah', '6A', '2025-03-16 09:52:07'),
(8, 'Nora', '6A', '2025-03-16 09:52:14'),
(9, 'Shinta', '6A', '2025-03-16 09:52:24'),
(10, 'Filaili', '6A', '2025-03-24 18:48:50'),
(14, 'Jannah', '6A', '2025-04-08 19:45:40'),
(15, 'Jefri', '6A', '2025-04-16 16:39:04');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('ADMIN','GURU') NOT NULL DEFAULT 'GURU',
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `password`, `role`, `created_at`) VALUES
(1, 'indah', 'pbkdf2:sha256:260000$4PVPXQLynb9UCTTB$549643856768c68b1b5136b7d37ddcb15ca300ebc58ba1d3d8a15b730427b18d', 'ADMIN', '2025-03-12 22:54:55'),
(2, 'admin2', 'pbkdf2:sha256:260000$ldFNVaZZ2TDr71Il$b5c729713b6a9b2b5b442af05c2bbe93816f546eab6438bbc2f4e54957ae078d', 'ADMIN', '2025-03-21 19:45:08'),
(3, 'guru1', 'pbkdf2:sha256:260000$rM4z7rJbaDhW6nFk$3e157869681ab278e3cc7eaed8a719923ab8cd5791f1da3a5693ccc2673e7cd4', 'GURU', '2025-03-21 19:45:31');

-- --------------------------------------------------------

--
-- Table structure for table `verification_logs`
--

CREATE TABLE `verification_logs` (
  `log_id` int(11) NOT NULL,
  `assignment_id` int(11) DEFAULT NULL,
  `student_id` int(11) NOT NULL,
  `similarity_score` float NOT NULL,
  `verifier_id` int(11) NOT NULL,
  `status` enum('PENDING','COCOK','TIDAK_COCOK') NOT NULL DEFAULT 'PENDING',
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `verification_logs`
--

INSERT INTO `verification_logs` (`log_id`, `assignment_id`, `student_id`, `similarity_score`, `verifier_id`, `status`, `created_at`) VALUES
(16, 31, 7, 0.323776, 1, 'TIDAK_COCOK', '2025-04-08 04:57:46'),
(17, 32, 7, 0.292708, 1, 'TIDAK_COCOK', '2025-04-08 20:10:05'),
(18, 32, 7, 0.292708, 1, 'TIDAK_COCOK', '2025-04-08 20:10:05'),
(19, NULL, 14, 0.230335, 3, 'TIDAK_COCOK', '2025-04-16 16:46:34'),
(20, NULL, 14, 0.230335, 3, 'TIDAK_COCOK', '2025-04-16 16:46:39'),
(21, 36, 14, 0.793374, 1, 'COCOK', '2025-04-16 19:17:59'),
(22, 37, 14, 0.96533, 1, 'COCOK', '2025-04-16 19:19:29'),
(23, 38, 14, 0.73506, 1, 'TIDAK_COCOK', '2025-04-16 19:20:29'),
(24, 39, 14, 0.905018, 1, 'COCOK', '2025-04-16 19:21:08'),
(25, 40, 14, 0.849738, 3, 'COCOK', '2025-04-16 19:44:27'),
(26, 41, 14, 0.570492, 1, 'TIDAK_COCOK', '2025-04-17 23:28:58'),
(27, 42, 14, 0.36048, 1, 'TIDAK_COCOK', '2025-04-17 23:30:32'),
(28, 43, 14, 0.833636, 1, 'COCOK', '2025-04-19 05:41:31'),
(29, NULL, 14, 0.811192, 1, 'COCOK', '2025-04-19 05:42:05'),
(30, 45, 14, 0.000359064, 1, 'TIDAK_COCOK', '2025-04-19 05:42:32');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indexes for table `assignments`
--
ALTER TABLE `assignments`
  ADD PRIMARY KEY (`assignment_id`),
  ADD KEY `student_id` (`student_id`);

--
-- Indexes for table `handwriting_samples`
--
ALTER TABLE `handwriting_samples`
  ADD PRIMARY KEY (`sample_id`),
  ADD KEY `handwriting_samples_ibfk_1` (`student_id`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`notification_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`student_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `verification_logs`
--
ALTER TABLE `verification_logs`
  ADD PRIMARY KEY (`log_id`),
  ADD KEY `assignment_id` (`assignment_id`),
  ADD KEY `student_id` (`student_id`),
  ADD KEY `verifier_id` (`verifier_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `assignments`
--
ALTER TABLE `assignments`
  MODIFY `assignment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT for table `handwriting_samples`
--
ALTER TABLE `handwriting_samples`
  MODIFY `sample_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=145;

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `notification_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `student_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `verification_logs`
--
ALTER TABLE `verification_logs`
  MODIFY `log_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `assignments`
--
ALTER TABLE `assignments`
  ADD CONSTRAINT `assignments_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`);

--
-- Constraints for table `handwriting_samples`
--
ALTER TABLE `handwriting_samples`
  ADD CONSTRAINT `handwriting_samples_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`);

--
-- Constraints for table `notifications`
--
ALTER TABLE `notifications`
  ADD CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `verification_logs`
--
ALTER TABLE `verification_logs`
  ADD CONSTRAINT `verification_logs_ibfk_1` FOREIGN KEY (`assignment_id`) REFERENCES `assignments` (`assignment_id`),
  ADD CONSTRAINT `verification_logs_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`),
  ADD CONSTRAINT `verification_logs_ibfk_3` FOREIGN KEY (`verifier_id`) REFERENCES `users` (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
