from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "sys_department" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL,
    "level" INT NOT NULL DEFAULT 1,
    "sort" INT NOT NULL DEFAULT 0,
    "status" INT NOT NULL DEFAULT 1,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "parent_id" INT REFERENCES "sys_department" ("id") ON DELETE SET NULL
);
COMMENT ON COLUMN "sys_department"."name" IS '部门名称';
COMMENT ON COLUMN "sys_department"."level" IS '层级';
COMMENT ON COLUMN "sys_department"."sort" IS '排序';
COMMENT ON COLUMN "sys_department"."status" IS '状态: 1=正常, 0=停用';
COMMENT ON TABLE "sys_department" IS '部门模型 - 支持树形结构';
CREATE TABLE IF NOT EXISTS "sys_menu" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL,
    "path" VARCHAR(200),
    "icon" VARCHAR(100),
    "sort" INT NOT NULL DEFAULT 0,
    "status" INT NOT NULL DEFAULT 1,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "parent_id" INT REFERENCES "sys_menu" ("id") ON DELETE SET NULL
);
COMMENT ON COLUMN "sys_menu"."name" IS '菜单名称';
COMMENT ON COLUMN "sys_menu"."path" IS '路由路径';
COMMENT ON COLUMN "sys_menu"."icon" IS '图标';
COMMENT ON COLUMN "sys_menu"."sort" IS '排序';
COMMENT ON COLUMN "sys_menu"."status" IS '状态: 1=正常, 0=停用';
COMMENT ON TABLE "sys_menu" IS '菜单模型 - 支持树形结构';
CREATE TABLE IF NOT EXISTS "sys_permission" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL,
    "code" VARCHAR(100) NOT NULL UNIQUE,
    "api_path" VARCHAR(200),
    "method" VARCHAR(10),
    "status" INT NOT NULL DEFAULT 1,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "menu_id" INT REFERENCES "sys_menu" ("id") ON DELETE SET NULL
);
COMMENT ON COLUMN "sys_permission"."name" IS '权限名称';
COMMENT ON COLUMN "sys_permission"."code" IS '权限编码';
COMMENT ON COLUMN "sys_permission"."api_path" IS 'API路径';
COMMENT ON COLUMN "sys_permission"."method" IS 'HTTP方法: GET/POST/PUT/DELETE/PATCH';
COMMENT ON COLUMN "sys_permission"."status" IS '状态: 1=正常, 0=停用';
COMMENT ON TABLE "sys_permission" IS '权限点模型';
CREATE TABLE IF NOT EXISTS "sys_position" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL,
    "code" VARCHAR(50) NOT NULL UNIQUE,
    "status" INT NOT NULL DEFAULT 1,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "sys_position"."name" IS '职位名称';
COMMENT ON COLUMN "sys_position"."code" IS '职位编码';
COMMENT ON COLUMN "sys_position"."status" IS '状态: 1=正常, 0=停用';
COMMENT ON TABLE "sys_position" IS '职位模型';
CREATE TABLE IF NOT EXISTS "sys_role" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL,
    "code" VARCHAR(50) NOT NULL UNIQUE,
    "description" VARCHAR(500),
    "status" INT NOT NULL DEFAULT 1,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "sys_role"."name" IS '角色名称';
COMMENT ON COLUMN "sys_role"."code" IS '角色编码';
COMMENT ON COLUMN "sys_role"."description" IS '描述';
COMMENT ON COLUMN "sys_role"."status" IS '状态: 1=正常, 0=停用';
COMMENT ON TABLE "sys_role" IS '角色模型';
CREATE TABLE IF NOT EXISTS "sys_user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(50) NOT NULL UNIQUE,
    "password_hash" VARCHAR(255) NOT NULL,
    "real_name" VARCHAR(100) NOT NULL,
    "email" VARCHAR(100),
    "phone" VARCHAR(20),
    "status" INT NOT NULL DEFAULT 1,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "department_id" INT REFERENCES "sys_department" ("id") ON DELETE SET NULL,
    "position_id" INT REFERENCES "sys_position" ("id") ON DELETE SET NULL
);
COMMENT ON COLUMN "sys_user"."username" IS '用户名';
COMMENT ON COLUMN "sys_user"."password_hash" IS '密码哈希';
COMMENT ON COLUMN "sys_user"."real_name" IS '真实姓名';
COMMENT ON COLUMN "sys_user"."email" IS '邮箱';
COMMENT ON COLUMN "sys_user"."phone" IS '手机号';
COMMENT ON COLUMN "sys_user"."status" IS '状态: 1=正常, 0=停用';
COMMENT ON TABLE "sys_user" IS '用户模型';
CREATE TABLE IF NOT EXISTS "oa_leave_request" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "leave_type" VARCHAR(50) NOT NULL,
    "start_date" DATE NOT NULL,
    "end_date" DATE NOT NULL,
    "reason" TEXT NOT NULL,
    "status" VARCHAR(20) NOT NULL DEFAULT 'draft',
    "approved_at" TIMESTAMPTZ,
    "approved_comment" TEXT,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "approver_id" INT REFERENCES "sys_user" ("id") ON DELETE SET NULL,
    "user_id" INT NOT NULL REFERENCES "sys_user" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "oa_leave_request"."leave_type" IS '请假类型: annual/病假/sick/事假/personal';
COMMENT ON COLUMN "oa_leave_request"."start_date" IS '开始日期';
COMMENT ON COLUMN "oa_leave_request"."end_date" IS '结束日期';
COMMENT ON COLUMN "oa_leave_request"."reason" IS '请假原因';
COMMENT ON COLUMN "oa_leave_request"."status" IS '状态: draft/pending/approved/rejected/cancelled';
COMMENT ON COLUMN "oa_leave_request"."approved_at" IS '审批时间';
COMMENT ON COLUMN "oa_leave_request"."approved_comment" IS '审批意见';
COMMENT ON TABLE "oa_leave_request" IS '请假单模型';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztnW1zmkoUx7+K46t2Jq2Irmhn7gub2Ca3eZrE3NvpwzALLIYbBArYNNPJd79nUeQZwa"
    "ig3Tc2Lucg/Pbscs6fhf5uTk2F6M7bE2Jh250Sw22+a/xuGnhK4I+UrUeNJrasYBttcLGk"
    "e+bOkyMqUVvJcW0s072qWHcINCnEkW3NcjXToD7fZgOO9OET0c8e5tvfZkjoS403DfiKeB"
    "U+Oxw09vptuknt8d9mAlE60CL0u/RHFFOGX9GMyYb2NzO0HzMiuuaEuPfEhr1+/Q7NmqGQ"
    "X8Txv1oPoqoRXYkA0xS6A69ddJ8sr+3McD94hvRQJVE29dnUCIytJ/feNJbW2hzchBjExi"
    "6hu3ftGQVnzHR9QdpnOT/SwGR+iCEfhah4plP81DtB328MAVw0yaZBew6OxvFOcEJ/5Q3f"
    "7grdfqfX7YOJdyTLFuF5fnrBuc8dPQKX4+aztx27eG7hYQy4ef8myB3fYzsdnW8fgweHHI"
    "fno8qj5zcE+IJgzeUXizbU5RQIpoHKxcMyg+oU/xJ1Ykzce/ja5rgchv8Mb45PhzevwOo1"
    "3bsJw2o+6i4Xm/j5Ngo6AKuTn0QvEZNL+9VhuSmy7TSsSO564xILBVFuJEADbo5puyWw+e"
    "a7o8alUet1BkANYlGtiJqL3ZlThtvSoeJ4E3ipB/w4rg0Gf8FfUq9DSXYACQffEYdksEJ8"
    "vxqysk0oBhGnROUJbHG1KUlHHPWMYVYWrm/9P3Y6fRa//MA5KFeG/rS4suWgG59djG7Hw4"
    "treiZTx/mhe4iG4xHdwnutT7HWV73YlLrcSePfs/Fpg35tfLm6HHkETced2N4vBnbjL016"
    "THjmmqJhPopYCV2E/VYfTKRjZ5ayZsdGPVnHVtqxi4MP+hWyYMiBxVIJYcRnrQlxcWC77M"
    "ENTHQ0nVYfUhPDOZIkww+mTbSJ8Yk8eSjP4JiwIaflhKk1TO0wPvux4LcGR2Hjx2WlEQ0R"
    "OEs4N+J653k7Gjcu787Pmx5OCcsPj9hWxAyu8r2mK7CrJNn3C88Pn26Ijr3zODSo0QnYIX"
    "ZKylIGwx3sYr8A0BAxeTMUGpGgSW6a8tN4CzbwxDtq+tv0lxY0Logxa6aoCF770Sr9YOpb"
    "FVAO+h0FkjLUQWgzysGL98eUA6YcFFYOwtFWQ+XAwrDvEmB9+7XAbmxqpFzBhJZqnbb/N1"
    "KTw70IV74QVz6HK5/kqslmylU3m6tvXzlX1FMJnfy4opLM9mOUqTRMpWEqDSvmmUrDOrZI"
    "xzKVpuYqjV8j1g7gfuoze4czOjiJPdUcB3b9Qn3mermj/YKxTZUmxCRFq4kSy1dsrKhtAd"
    "2mJ3QhbRv0EAfJGicNwmpLiiyzypypLkx1KVzFhoOphqqLDGOsDFjffjNg1wzL+BhV21Cl"
    "CX2uXRus2NLEsoJW2Kdi8WV4fVZLLWsKE66ZMoVmQw08KkZ6Oh5fU1nfu5zICnrX+Dgat6"
    "6vbuHjbtw6GZ2PxqPW9XB8fLpeFBcK4pwYTmhdTLVhqs0Wss+DKe6ZanOgHZsoDOk94nKa"
    "TciDKTY+EKbXRAKjtFqz1fLcdDQ3qzj3tx2tLM3DlkUWVHBduBJ31a6yoiTPNmTFOCvGi9"
    "+qD4URK8Y3VoyHsb6sGEdFqKJsqIiVMVueFlgZc2DZLitjDrRjl7d0EknkqpuBbInyhrPr"
    "G9M720Rm7bWvzKpt36pIRj1QePjkBX5VRp1pyDJqllEXz6hDYcQy6s1l1CGsdcuowwdbAm"
    "3MrfLlxb2OrAJidb1oRYWiFeVEK0pZXsxqFVarbCHnOZiUltUqB9qxZWuVbSbrXumSkqz7"
    "JU1+sj7zrQok63Q+hLmS7wgrkvVsQ5as7zxZpz1cNmEP+1SdW4aDiabs9cgqLew4jyaM3X"
    "vslHwOMOZYfVGEJHmRsVPCMn1TE+HkdTjzCBVZRYVQ9ioqui2KGi4aulg2giNO1SMWhDZd"
    "nCYNCHwO6DPR64byVupOMsVaymuwsvEuHSqviwYcBqaCJNVnNaUFREoF69Khcpo9vivR1a"
    "odTB+9Vtd6lJUvtpIyZyElKzRZocnqEVZoso5NrO0L3h9bboVfwu8PWucXuTYvlnyVfKY1"
    "6vUHsctZIxl9lfELV0ru6auyjmLrJRPDLGPVZFpIboBieOnj3jKMDbYXPCWMLcs2f8K1TC"
    "f4J3nhEoFzuo8bArSc/YrRSLB5JER7fhq7JVJBHlDJ6okIlhRhNo4tW6A1sRjpr6JCbV9S"
    "qVjGdYXk69pS5NpV5ky03bloO+92j0GCX7aOEPWqXvUKB5YgC9I8pN41sGHMsN6iha+M5g"
    "YtR5MfoKVL+tKixSK2YxpYr4fgC5de2xVp2ZNeUGUKESGvvGJq56KvytFHvAcy1XsQoYNe"
    "aBd841YOW1oixcVFQynNLexTJ2r++yyRum1qUME6aTnhmPzKmD4Dj3qNfNQZUO27RwquXM"
    "kr1kefx5E63R+xry6Gn19HavXzq8uPvnlohB+fX70vqC5mz7OZ8uIWSTcVG6vepTBXZPSs"
    "YOo0FEDc8hPglk3+IzIcUEumBYSuk7XuPWxe2V1m6OV1qpjrBoSqjb4NUsL0Vbi8QJ+fR2"
    "qP/h8oasE3E+yJWuXDyNUhl70km9N0qSB7QkvzrfwOSaRj2xxdkzeQC9572vXMxtT9gxCB"
    "mbp/oB2bUGcWM55dTp2Oef1B6nT8Pyooxy3ksbvbxNVDy5H0/dWAL5ShCz5NVSNB8CimQY"
    "dCI6I/Hw9vj4cno2bqqN0dufqIy3FwsbmoVi+NGBJbk++bKZLsYstRnhiLA5tVEmw2VSal"
    "7lxKhWB0Uu+uZdf3IZeKpZTiFLe/DpMOjRIQF+b7CXBLT/cZbmoJ/Pft1WXWA35LlxjIOw"
    "NO8Kuiye5RQ9cc93s9seZQpGedX/LGq9tYvk138D4todnl5eX5f3ta6fE="
)
