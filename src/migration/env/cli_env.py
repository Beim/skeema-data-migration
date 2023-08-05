from . import common

MIGRATION_CWD = common.getenv("MIGRATION_CWD", default=".", required=False)
MYSQL_PWD = common.getenv("MYSQL_PWD", required=True)

ALLOW_UNSAFE = int(common.getenv("ALLOW_UNSAFE", default="0", required=False))
ALLOW_ECHO_SQL = int(common.getenv("ALLOW_ECHO_SQL", default="0", required=False))

SKEEMA_CMD_PATH = common.getenv("SKEEMA_CMD_PATH", default="skeema", required=False)
NODE_CMD_PATH = common.getenv("NODE_CMD_PATH", default="node", required=False)
NPM_CMD_PATH = common.getenv("NPM_CMD_PATH", default="npm", required=False)

SCHEMA_DIR = "schema"
DATA_DIR = "data"
MIGRATION_PLAN_DIR = "migration_plan"
SCHEMA_STORE_DIR = ".schema_store"
ENV_INI_FILE = "env.ini"

TABLE_MIGRATION_HISTORY = common.getenv(
    "TABLE_MIGRATION_HISTORY", default="_migration_history", required=False
)
TABLE_MIGRATION_HISTORY_LOG = common.getenv(
    "TABLE_MIGRATION_HISTORY", default="_migration_history_log", required=False
)

# TODO*: use ORM in the example
SAMPLE_PYTHON_FILE = """from sqlalchemy.orm import Session
from sqlalchemy import text

def run(session: Session, args: dict) -> int:
    with session.begin():
        session.execute(text("INSERT INTO `testtable` (`id`, `name`) VALUES (1, 'foo.bar');"))
        return 0
"""  # noqa

SAMPLE_SHELL_FILE = """#!/bin/sh
mysql -u$USER -p$MYSQL_PWD -h$HOST -P$PORT -D$SCHEMA -e "INSERT INTO \`testtable\` (\`id\`, \`name\`) VALUES (1, 'foo.bar');"
"""  # noqa

# .gitignore
SAMPLE_GIT_IGNORE = """# generated by schema-data-migration
.skeema
env.ini
node_modules/
build/
tmp/
data/*.js
data/*.js.map
"""  # noqa

# .git/hooks/pre-commit
SAMPLE_PRE_COMMIT = """# generated by schema-data-migration
echo "Running pre-commit hook"

echo "> sdm check integrity"
sdm check integrity || exit 1

echo "> sdm clean store --dry-run --skip-integrity"
sdm clean store --dry-run --skip-integrity
if [ $? -ne 0 ]; then
    echo "Please run 'sdm clean store' to remove any out of source control files"
    exit 1
fi
"""  # noqa

SAMPLE_DOT_ENV = """# generated by schema-data-migration
MYSQL_PWD="%s"
SKEEMA_CMD_PATH="skeema"
NODE_CMD_PATH="node"
NPM_CMD_PATH="npm"
ALLOW_ECHO_SQL=0
LOG_LEVEL="INFO"
"""

SAMPLE_PCKAGE_JSON = """{
  "name": "schema-data-migration-example",
  "version": "0.0.1",
  "description": "Example how to use schema-data-migration with TypeORM.",
  "license": "MIT",
  "readmeFilename": "README.md",
  "devDependencies": {
    "@types/node": "^17.0.21",
    "prettier": "^2.5.1",
    "typescript": "^4.6.2"
  },
  "dependencies": {
    "mysql": "^2.18.1",
    "reflect-metadata": "^0.1.13",
    "typeorm": "^0.3.0-rc.40"
  },
  "scripts": {
    "start": "tsc && node src/index.js",
    "build": "tsc"
  }
}
"""

SAMPLE_TSCONFIG_JSON = """{
  "version": "2.4.2",
  "compilerOptions": {
    "lib": [
      "es5",
      "es6"
    ],
    "target": "es6",
    "module": "commonjs",
    "moduleResolution": "node",
    "emitDecoratorMetadata": true,
    "experimentalDecorators": true,
    "sourceMap": true
  },
  "exclude": [
    "node_modules"
  ]
}
"""

SAMPLE_INDEX_TS = """import { DataSource } from "typeorm"
import { Entities, Run } from "./migration"

export const AppDataSource = new DataSource({
  type: "mysql",
  host: process.env.HOST,
  port: parseInt(process.env.PORT),
  username: process.env.USER,
  password: process.env.MYSQL_PWD,
  database: process.env.SCHEMA,
  synchronize: false,
  logging: %s,
  entities: Entities,
  subscribers: [],
  migrations: [],
})

async function main() {
  try {
    await AppDataSource.initialize()
  } catch (e) {
    console.log("AppDataSource initialize failed")
    console.log(e)
    process.exit(1)
  }

  try {
    let args = {
      "SDM_CHECKSUM_MATCH": process.env.SDM_CHECKSUM_MATCH,
    }
    const result = await Run(AppDataSource, args)
    if ("SDM_EXPECTED" in process.env) {
      if (parseInt(process.env.SDM_EXPECTED) !== result) {
        throw new Error(`Expected ${process.env.SDM_EXPECTED} but got ${result}`)
      }
    }
  } catch (e) {
    console.log("Migration failed")
    console.log(e)
    process.exit(1)
  }
  process.exit(0)
}

main()
"""

SAMPLE_MIGRATION_TS = """import { Column, PrimaryColumn, Entity, DataSource } from "typeorm"

@Entity()
class Testtable {
  @PrimaryColumn()
  id: number

  @Column()
  name: string
}

export const Entities = [Testtable]

export const Run = async (datasource: DataSource, args: { [key: string]: string }): Promise<number> => {
    await datasource.manager.insert(Testtable, { id: 1, name: "foo" })
    return 0
}
"""  # noqa
