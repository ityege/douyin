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

 Date: 21/09/2024 06:36:01
*/


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
-- Records of conf
-- ----------------------------
INSERT INTO "luzhi"."conf" VALUES ('douyin_delete_path', '删除指定的目录', 'root_path', '根目录', 'F:\抖音录制', NULL);
INSERT INTO "luzhi"."conf" VALUES ('douyin_mv_path', '移动指定的目录', 'source_directory', '源路径', 'F:\抖音录制', NULL);
INSERT INTO "luzhi"."conf" VALUES ('douyin_mv_path', '移动指定的目录', 'destination_directory', '目的路径', 'E:\抖音录制', '');
INSERT INTO "luzhi"."conf" VALUES ('douyin_mv_path', '移动指定的目录', 'mv_list', '需要移动的目录', 'a,b,c', '中间使用逗号隔开');
INSERT INTO "luzhi"."conf" VALUES ('znl', '快手直播录制', 'download_path', '下载路径', 'D:\正能量', NULL);
INSERT INTO "luzhi"."conf" VALUES ('douyin_record', NULL, 'add_task_is_log', NULL, '0', NULL);
INSERT INTO "luzhi"."conf" VALUES ('douyin_record', NULL, 'run_now_is_log', '', '0', NULL);
INSERT INTO "luzhi"."conf" VALUES ('kuaishou_record', '快手录制', 'cookie', NULL, '', NULL);
INSERT INTO "luzhi"."conf" VALUES ('douyin_delete_path', '删除指定的目录', 'delete_list', '删除指定目录', 'a,b,c', '中间用逗号隔开');
INSERT INTO "luzhi"."conf" VALUES ('douyin_record', '抖音直播录制程序', 'download_path', '下载路径', 'D:\抖音录制', NULL);
INSERT INTO "luzhi"."conf" VALUES ('record', '录制', 'iscache', '是否缓存', '0', NULL);
INSERT INTO "luzhi"."conf" VALUES ('douyin_record', NULL, 'list_task_is_log', NULL, '1', NULL);
INSERT INTO "luzhi"."conf" VALUES ('record', '录制', 'isstop', '是否停止', '0', NULL);
INSERT INTO "luzhi"."conf" VALUES ('douyin_record', '抖音录制', 'cookie', NULL, '', NULL);

-- ----------------------------
-- Primary Key structure for table conf
-- ----------------------------
ALTER TABLE "luzhi"."conf" ADD CONSTRAINT "conf_pkey" PRIMARY KEY ("program", "key");
