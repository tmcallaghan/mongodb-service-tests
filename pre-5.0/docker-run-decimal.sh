#!/usr/bin/env bash
if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters"
    echo "Usage : $0 [URI of MongoDB Atlas, AWS Document DB, or Azure Cosmos DB] [Version to test, either 4.0, 4.2, or 4.4]"
    exit 1
fi
if [[ $2 != "4.0" ]] && [[ $2 != "4.2" ]] && [[ $2 != "4.4" ]] ; then
    echo "Invalid version; must be 4.0, 4.2, or 4.4. Please use the post-5.0 directory for running versions 5.0 and beyond."
fi

URI=$1
VERSION=$2
LOCAL_RESULTS_DIR="$(pwd)/results-${VERSION}"
IMAGE="mongo/mongodb-tests:${VERSION}"
rm -rf ${LOCAL_RESULTS_DIR}
mkdir ${LOCAL_RESULTS_DIR}

echo "Starting test suite - Decimal"
docker run --name mongodb-tests-decimal-${VERSION} -e "URI=${URI}" -v ${LOCAL_RESULTS_DIR}:/results ${IMAGE} decimal > /dev/null
docker logs mongodb-tests-decimal-${VERSION} > ${LOCAL_RESULTS_DIR}/stdout_decimal.log
docker rm -v mongodb-tests-decimal-${VERSION}
echo "Decimal tests complete"

