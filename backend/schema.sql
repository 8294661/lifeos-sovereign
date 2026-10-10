-- LifeOS 数据库表结构（仅结构，不含任何数据）
-- 自动生成，来源：SHOW CREATE TABLE

SET NAMES utf8mb4;

-- 表：daily_records
CREATE TABLE `daily_records` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `record_date` date NOT NULL,
  `study_minutes` int DEFAULT '0',
  `creation_minutes` int DEFAULT '0',
  `reading_minutes` int DEFAULT '0',
  `exercise_minutes` int DEFAULT '0',
  `sleep_hours` decimal(4,2) DEFAULT NULL,
  `mood_score` tinyint DEFAULT NULL,
  `energy_score` tinyint DEFAULT NULL,
  `summary` text COLLATE utf8mb4_unicode_ci,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`record_date`),
  CONSTRAINT `daily_records_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `daily_records_chk_1` CHECK ((`study_minutes` >= 0)),
  CONSTRAINT `daily_records_chk_2` CHECK ((`creation_minutes` >= 0)),
  CONSTRAINT `daily_records_chk_3` CHECK ((`reading_minutes` >= 0)),
  CONSTRAINT `daily_records_chk_4` CHECK ((`exercise_minutes` >= 0)),
  CONSTRAINT `daily_records_chk_5` CHECK (((`sleep_hours` is null) or (`sleep_hours` between 0 and 24))),
  CONSTRAINT `daily_records_chk_6` CHECK (((`mood_score` is null) or (`mood_score` between 1 and 10))),
  CONSTRAINT `daily_records_chk_7` CHECK (((`energy_score` is null) or (`energy_score` between 1 and 10)))
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 表：family_members
CREATE TABLE `family_members` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `relationship` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `birthday` date DEFAULT NULL,
  `occupation` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `family_members_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 表：goals
CREATE TABLE `goals` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `parent_goal_id` int DEFAULT NULL,
  `title` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `goal_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `priority` int DEFAULT '3',
  `progess` decimal(5,2) DEFAULT '0.00',
  `status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'not_started',
  `start_date` date DEFAULT NULL,
  `deadline` date DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `parent_goal_id` (`parent_goal_id`),
  CONSTRAINT `goals_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `goals_ibfk_2` FOREIGN KEY (`parent_goal_id`) REFERENCES `goals` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 表：health_profile
CREATE TABLE `health_profile` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `blood_type` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `allergies` text COLLATE utf8mb4_unicode_ci,
  `health_status` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `exercise_habit` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `health_profile_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 表：personal_info
CREATE TABLE `personal_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `height` decimal(5,2) DEFAULT NULL,
  `current_weight` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_personal_user` (`user_id`),
  CONSTRAINT `personal_info_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 表：user
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `gender` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

