/*
 Navicat Premium Data Transfer

 Source Server         : 本地postgre
 Source Server Type    : PostgreSQL
 Source Server Version : 140013
 Source Host           : 127.0.0.1:5432
 Source Catalog        : postgres
 Source Schema         : luzhi

 Target Server Type    : PostgreSQL
 Target Server Version : 140013
 File Encoding         : 65001

 Date: 01/03/2025 00:11:06
*/


-- ----------------------------
-- Sequence structure for table_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "luzhi"."table_id_seq";
CREATE SEQUENCE "luzhi"."table_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Table structure for auto_record
-- ----------------------------
DROP TABLE IF EXISTS "luzhi"."auto_record";
CREATE TABLE "luzhi"."auto_record" (
  "id" varchar COLLATE "pg_catalog"."default" NOT NULL,
  "name" varchar COLLATE "pg_catalog"."default",
  "logic_delete" int2,
  "platform" varchar COLLATE "pg_catalog"."default" NOT NULL,
  "run_now" int2,
  "core_guard" int2,
  "core_guard_start_time" varchar COLLATE "pg_catalog"."default",
  "core_guard_end_time" varchar COLLATE "pg_catalog"."default",
  "last_record_time" varchar COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "luzhi"."auto_record"."id" IS '抖音用户id';
COMMENT ON COLUMN "luzhi"."auto_record"."name" IS '抖音用户名称';
COMMENT ON COLUMN "luzhi"."auto_record"."logic_delete" IS '0未删除,1删除';
COMMENT ON COLUMN "luzhi"."auto_record"."platform" IS '平台,目前只支持b站和抖音';
COMMENT ON COLUMN "luzhi"."auto_record"."run_now" IS '是否立即运行';

-- ----------------------------
-- Table structure for conf
-- ----------------------------
DROP TABLE IF EXISTS "luzhi"."conf";
CREATE TABLE "luzhi"."conf" (
  "program" varchar COLLATE "pg_catalog"."default" NOT NULL,
  "program_comment" varchar COLLATE "pg_catalog"."default",
  "key" varchar COLLATE "pg_catalog"."default" NOT NULL,
  "key_comment" varchar COLLATE "pg_catalog"."default",
  "value" varchar COLLATE "pg_catalog"."default",
  "value_comment" varchar COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "luzhi"."conf"."program" IS '程序名称';
COMMENT ON COLUMN "luzhi"."conf"."program_comment" IS '程序名称注释';
COMMENT ON COLUMN "luzhi"."conf"."key" IS '配置key';
COMMENT ON COLUMN "luzhi"."conf"."key_comment" IS '配置key说明';
COMMENT ON COLUMN "luzhi"."conf"."value" IS '配置value';
COMMENT ON COLUMN "luzhi"."conf"."value_comment" IS '配置value说明';
COMMENT ON TABLE "luzhi"."conf" IS '配置文件表';

-- ----------------------------
-- Table structure for film_status
-- ----------------------------
DROP TABLE IF EXISTS "luzhi"."film_status";
CREATE TABLE "luzhi"."film_status" (
  "id" varchar COLLATE "pg_catalog"."default" NOT NULL,
  "film_up" varchar COLLATE "pg_catalog"."default",
  "film_status" varchar COLLATE "pg_catalog"."default",
  "record_command" varchar COLLATE "pg_catalog"."default",
  "record_film_path" varchar COLLATE "pg_catalog"."default",
  "record_process_id" varchar COLLATE "pg_catalog"."default",
  "record_time_start_unix" float8,
  "record_time_start_string" varchar COLLATE "pg_catalog"."default",
  "record_time_end_unix" float8,
  "record_time_end_string" varchar COLLATE "pg_catalog"."default",
  "record_spend_time_unix" float8,
  "record_spend_time_string" varchar COLLATE "pg_catalog"."default",
  "transcode_command" varchar COLLATE "pg_catalog"."default",
  "transcode_film_path" varchar COLLATE "pg_catalog"."default",
  "transcode_process_id" varchar COLLATE "pg_catalog"."default",
  "transcode_time_start_unix" float8,
  "transcode_time_start_string" varchar COLLATE "pg_catalog"."default",
  "transcode_time_end_unix" float8,
  "transcode_time_end_string" varchar COLLATE "pg_catalog"."default",
  "transcode_spend_time_unix" float8,
  "transcode_spend_time_string" varchar COLLATE "pg_catalog"."default",
  "logic_delete" int2
)
;
COMMENT ON COLUMN "luzhi"."film_status"."id" IS '视频id';
COMMENT ON COLUMN "luzhi"."film_status"."film_up" IS '视频博主';
COMMENT ON COLUMN "luzhi"."film_status"."film_status" IS '视频状态';
COMMENT ON COLUMN "luzhi"."film_status"."record_command" IS '录制命令';
COMMENT ON COLUMN "luzhi"."film_status"."record_film_path" IS '录制视频路径';
COMMENT ON COLUMN "luzhi"."film_status"."record_process_id" IS '录制进程id';
COMMENT ON COLUMN "luzhi"."film_status"."record_time_start_unix" IS '录制开始时间时间戳';
COMMENT ON COLUMN "luzhi"."film_status"."record_time_start_string" IS '录制开始时间字符串';
COMMENT ON COLUMN "luzhi"."film_status"."record_time_end_unix" IS '录制结束时间时间戳';
COMMENT ON COLUMN "luzhi"."film_status"."record_time_end_string" IS '录制结束时间字符串';
COMMENT ON COLUMN "luzhi"."film_status"."record_spend_time_unix" IS '录制时长时间戳';
COMMENT ON COLUMN "luzhi"."film_status"."record_spend_time_string" IS '录制时长字符串';
COMMENT ON COLUMN "luzhi"."film_status"."transcode_command" IS '转码命令';
COMMENT ON COLUMN "luzhi"."film_status"."transcode_film_path" IS '转码视频路径';
COMMENT ON COLUMN "luzhi"."film_status"."transcode_process_id" IS '转码进程id';
COMMENT ON COLUMN "luzhi"."film_status"."transcode_time_start_unix" IS '转码开始时间时间戳';
COMMENT ON COLUMN "luzhi"."film_status"."transcode_time_start_string" IS '转码开始时间字符串';
COMMENT ON COLUMN "luzhi"."film_status"."transcode_time_end_unix" IS '转码结束时间时间戳';
COMMENT ON COLUMN "luzhi"."film_status"."transcode_time_end_string" IS '转码结束时间字符串';
COMMENT ON COLUMN "luzhi"."film_status"."transcode_spend_time_unix" IS '转码时长时间戳';
COMMENT ON COLUMN "luzhi"."film_status"."transcode_spend_time_string" IS '转码时长字符串';
COMMENT ON COLUMN "luzhi"."film_status"."logic_delete" IS '逻辑删除 0未删除 1删除';
COMMENT ON TABLE "luzhi"."film_status" IS '视频录制状态表';

-- ----------------------------
-- Table structure for options
-- ----------------------------
DROP TABLE IF EXISTS "luzhi"."options";
CREATE TABLE "luzhi"."options" (
  "option" varchar COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Table structure for short_film
-- ----------------------------
DROP TABLE IF EXISTS "luzhi"."short_film";
CREATE TABLE "luzhi"."short_film" (
  "id" varchar COLLATE "pg_catalog"."default" NOT NULL,
  "film_up" varchar COLLATE "pg_catalog"."default",
  "path" varchar COLLATE "pg_catalog"."default",
  "film_length_unix" float8,
  "film_length_string" varchar COLLATE "pg_catalog"."default",
  "if_delete" varchar COLLATE "pg_catalog"."default",
  "logic_delete" int2
)
;
COMMENT ON COLUMN "luzhi"."short_film"."id" IS '视频id';
COMMENT ON COLUMN "luzhi"."short_film"."film_up" IS '视频博主';
COMMENT ON COLUMN "luzhi"."short_film"."path" IS '输出路径';
COMMENT ON COLUMN "luzhi"."short_film"."film_length_unix" IS '视频长度unix';
COMMENT ON COLUMN "luzhi"."short_film"."film_length_string" IS '视频长度string';
COMMENT ON COLUMN "luzhi"."short_film"."if_delete" IS '是否删除 删除';
COMMENT ON COLUMN "luzhi"."short_film"."logic_delete" IS '逻辑删除 0未删除，1删除';

-- ----------------------------
-- Table structure for subprocess_status
-- ----------------------------
DROP TABLE IF EXISTS "luzhi"."subprocess_status";
CREATE TABLE "luzhi"."subprocess_status" (
  "id" varchar COLLATE "pg_catalog"."default" NOT NULL,
  "status" varchar COLLATE "pg_catalog"."default",
  "film_up" varchar COLLATE "pg_catalog"."default",
  "index" int8,
  "logic_delete" int2,
  "film_length_unix" float8,
  "film_length_string" varchar COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "luzhi"."subprocess_status"."id" IS '视频id';
COMMENT ON COLUMN "luzhi"."subprocess_status"."status" IS '状态 运行中 已结束 强制结束';
COMMENT ON COLUMN "luzhi"."subprocess_status"."index" IS '对应的调度进程';
COMMENT ON COLUMN "luzhi"."subprocess_status"."logic_delete" IS '逻辑删除字段 0 未删除，1删除';
COMMENT ON TABLE "luzhi"."subprocess_status" IS '进程状态表';

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
SELECT setval('"luzhi"."table_id_seq"', 2, true);

-- ----------------------------
-- Primary Key structure for table auto_record
-- ----------------------------
ALTER TABLE "luzhi"."auto_record" ADD CONSTRAINT "auto_record_pkey" PRIMARY KEY ("id", "platform");

-- ----------------------------
-- Primary Key structure for table conf
-- ----------------------------
ALTER TABLE "luzhi"."conf" ADD CONSTRAINT "conf_pkey" PRIMARY KEY ("program", "key");

-- ----------------------------
-- Primary Key structure for table film_status
-- ----------------------------
ALTER TABLE "luzhi"."film_status" ADD CONSTRAINT "film_status_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table subprocess_status
-- ----------------------------
ALTER TABLE "luzhi"."subprocess_status" ADD CONSTRAINT "subprocess_status_pkey" PRIMARY KEY ("id");
