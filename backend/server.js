const express = require('express');
const neo4j = require('neo4j-driver');
const cors = require('cors');

require('dotenv').config({ path: '../.env' });

const app = express();
const port = 3000;

const URI = process.env.NEO4J_URI;
const USER = process.env.NEO4J_USERNAME;
const PASSWORD = process.env.NEO4J_PASSWORD;

app.use(cors())

app.get('/path', async (req, res) => {
    const source = req.query.source;
    const target = req.query.target;

    if (!source || !target) return res.status(400).send("Missing Required Parameters");
    if (source == target) return res.status(401).send("Made it!");

    const driver = neo4j.driver(URI, neo4j.auth.basic(USER, PASSWORD));

    const { records, summary } = await driver.executeQuery(`
            MATCH p = shortestPath(
            (start:Article {name: $source})
            -[:parent_of*..5]->
            (end:Article {name: $target})
            )

            RETURN p
        `,
        { source, target },
        { database: 'wikirace' }
    );

    if (records.length != 1) return res.status(400).send("Bad parameters.")

    const path = records[0].get("p");
    const { segments } = path;
    const next = segments[0].end.properties.name;
    const distance = path.segments.length;

    driver.close();

    return res.status(200).json({ next, distance });
})

app.listen(port, () => {
    console.log(`Listening on port ${port}`)
})
