const Discord = require("discord.js") // Require the library this is built in
const client = new Discord.Client({intents: new Discord.Intents(32767)}) // Make a new discord client with all intents
const TOKEN = process.env.token // Let the program know what bot we want to login with
const prefix = "~" // Tell the program what prefix we want to use

const fun = require("./commands/Fun/fun") // Require our fun commands.
const search = require("./commands/Google search/search") // Require our search commands

client.on("ready", () => {
    console.log("Ready!") // Say that we are ready so we know when to use our bot
})

client.on("messageCreate", async msg => {
    fun.useCommands(msg, prefix)
    search.useCommands(msg, prefix)
})

client.login(TOKEN) // Login to our bot with our token
