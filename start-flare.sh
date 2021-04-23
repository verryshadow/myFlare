export COMPOSE_PROJECT=codex-develop

cd ..
baseDir=$(pwd)
cd codex-flare
CODEX_REPOS=${CODEX_REPOS:-"codex-keycloak,codex-feasibility-gui,codex-feasibility-backend,codex-flare"}
export FLARE_DEBUG=--debug

export CODEX_CONCEPT_TREE_PATH=${CODEX_CONCEPT_TREE_PATH:-"$baseDir/ontology/codex-code-tree.json"}
export CODEX_TERM_CODE_MAPPING_PATH=${CODEX_TERM_CODE_MAPPING_PATH:-"$baseDir/ontology/term-code-mapping.json"}


echo "export CODEX_CONCEPT_TREE_PATH=$CODEX_CONCEPT_TREE_PATH"
echo "export CODEX_TERM_CODE_MAPPING_PATH=$CODEX_TERM_CODE_MAPPING_PATH"
docker-compose -p $COMPOSE_PROJECT up -d