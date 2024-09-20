/*
 Navicat Premium Data Transfer

 Source Server         : 本地postgre
 Source Server Type    : PostgreSQL
 Source Server Version : 140013
 Source Host           : 127.0.0.1:5432
 Source Catalog        : postgres
 Source Schema         : paqu

 Target Server Type    : PostgreSQL
 Target Server Version : 140013
 File Encoding         : 65001

 Date: 21/09/2024 06:38:06
*/


-- ----------------------------
-- Sequence structure for download_over_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "paqu"."download_over_id_seq";
CREATE SEQUENCE "paqu"."download_over_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for paqu_list_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "paqu"."paqu_list_id_seq";
CREATE SEQUENCE "paqu"."paqu_list_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Table structure for conf
-- ----------------------------
DROP TABLE IF EXISTS "paqu"."conf";
CREATE TABLE "paqu"."conf" (
  "program" varchar COLLATE "pg_catalog"."default" NOT NULL,
  "program_comment" varchar COLLATE "pg_catalog"."default",
  "key" varchar COLLATE "pg_catalog"."default" NOT NULL,
  "key_comment" varchar COLLATE "pg_catalog"."default",
  "value" varchar COLLATE "pg_catalog"."default",
  "value_comment" varchar COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "paqu"."conf"."program" IS '程序名称';
COMMENT ON COLUMN "paqu"."conf"."program_comment" IS '程序名称注释';
COMMENT ON COLUMN "paqu"."conf"."key" IS '配置key';
COMMENT ON COLUMN "paqu"."conf"."key_comment" IS '配置key说明';
COMMENT ON COLUMN "paqu"."conf"."value" IS '配置value';
COMMENT ON COLUMN "paqu"."conf"."value_comment" IS '配置value说明';
COMMENT ON TABLE "paqu"."conf" IS '配置文件表';

-- ----------------------------
-- Table structure for download_over
-- ----------------------------
DROP TABLE IF EXISTS "paqu"."download_over";
CREATE TABLE "paqu"."download_over" (
  "id" int8 NOT NULL DEFAULT nextval('"paqu".download_over_id_seq'::regclass),
  "film_up" varchar COLLATE "pg_catalog"."default",
  "url" varchar COLLATE "pg_catalog"."default",
  "time_unix" float8,
  "time_string" varchar COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "paqu"."download_over"."id" IS '主键';
COMMENT ON COLUMN "paqu"."download_over"."film_up" IS '视频博主';
COMMENT ON COLUMN "paqu"."download_over"."url" IS '下载url';
COMMENT ON COLUMN "paqu"."download_over"."time_unix" IS '下载完成时间';
COMMENT ON COLUMN "paqu"."download_over"."time_string" IS '下载完成时间';

-- ----------------------------
-- Table structure for film_status
-- ----------------------------
DROP TABLE IF EXISTS "paqu"."film_status";
CREATE TABLE "paqu"."film_status" (
  "id" varchar COLLATE "pg_catalog"."default" NOT NULL,
  "film_up_id" varchar COLLATE "pg_catalog"."default",
  "download_url" varchar COLLATE "pg_catalog"."default",
  "download_path" varchar COLLATE "pg_catalog"."default",
  "download_time_unix" float8,
  "download_time_string" varchar COLLATE "pg_catalog"."default",
  "type1" varchar COLLATE "pg_catalog"."default",
  "download_id" int8,
  "is_download_success" int2,
  "status" varchar COLLATE "pg_catalog"."default",
  "desc1" varchar COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "paqu"."film_status"."id" IS '视频或者图片唯一id';
COMMENT ON COLUMN "paqu"."film_status"."film_up_id" IS '博主id';
COMMENT ON COLUMN "paqu"."film_status"."download_url" IS '下载url';
COMMENT ON COLUMN "paqu"."film_status"."download_path" IS '保存路径';
COMMENT ON COLUMN "paqu"."film_status"."download_time_unix" IS '下载时间';
COMMENT ON COLUMN "paqu"."film_status"."download_time_string" IS '下载时间';
COMMENT ON COLUMN "paqu"."film_status"."type1" IS '元素类型';
COMMENT ON COLUMN "paqu"."film_status"."download_id" IS '下载id';
COMMENT ON COLUMN "paqu"."film_status"."is_download_success" IS '是否下载成功';
COMMENT ON COLUMN "paqu"."film_status"."status" IS '状态';
COMMENT ON COLUMN "paqu"."film_status"."desc1" IS '文案';

-- ----------------------------
-- Table structure for paqu_list
-- ----------------------------
DROP TABLE IF EXISTS "paqu"."paqu_list";
CREATE TABLE "paqu"."paqu_list" (
  "id" int8 NOT NULL DEFAULT nextval('"paqu".paqu_list_id_seq'::regclass),
  "film_up" varchar COLLATE "pg_catalog"."default" NOT NULL,
  "url" varchar COLLATE "pg_catalog"."default" NOT NULL,
  "logic_delete" int2
)
;
COMMENT ON COLUMN "paqu"."paqu_list"."id" IS '录制任务列表';
COMMENT ON COLUMN "paqu"."paqu_list"."film_up" IS '博主名称';
COMMENT ON COLUMN "paqu"."paqu_list"."url" IS '主页url';
COMMENT ON COLUMN "paqu"."paqu_list"."logic_delete" IS '是否删除0未删除1删除';

-- ----------------------------
-- View structure for paqu_list_all
-- ----------------------------
DROP VIEW IF EXISTS "paqu"."paqu_list_all";
CREATE VIEW "paqu"."paqu_list_all" AS  SELECT download_over.film_up
   FROM paqu.download_over
UNION ALL
 SELECT paqu_list.film_up
   FROM paqu.paqu_list;

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "paqu"."download_over_id_seq"
OWNED BY "paqu"."download_over"."id";
SELECT setval('"paqu"."download_over_id_seq"', 300, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "paqu"."paqu_list_id_seq"
OWNED BY "paqu"."paqu_list"."id";
SELECT setval('"paqu"."paqu_list_id_seq"', 487, true);

-- ----------------------------
-- Primary Key structure for table conf
-- ----------------------------
ALTER TABLE "paqu"."conf" ADD CONSTRAINT "conf_pkey" PRIMARY KEY ("program", "key");

-- ----------------------------
-- Primary Key structure for table download_over
-- ----------------------------
ALTER TABLE "paqu"."download_over" ADD CONSTRAINT "download_over_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table film_status
-- ----------------------------
ALTER TABLE "paqu"."film_status" ADD CONSTRAINT "film_status_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table paqu_list
-- ----------------------------
ALTER TABLE "paqu"."paqu_list" ADD CONSTRAINT "paqu_list_pkey" PRIMARY KEY ("id");
