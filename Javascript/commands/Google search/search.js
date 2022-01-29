const Discord = require("discord.js")
const google = require("googlethis")

async function useCommands(msg, prefix) {
    if (msg.content.toLowerCase().startsWith(prefix + "search")) {
        if (msg.content.substring(prefix.length + "search".length) === "") {
            return msg.channel.send("Please specify a search!\nUsage: ```" + prefix + "search <query>```")
        } // Check if the person that used it didn't specify a query

        let message = undefined

        msg.channel.send("Searching... 🔍").then(m => {
            message = m
        }) // Send a message and make the message variable m so we can edit it later

        const options = {
            page: 0,
            safe: true,
            additional_params: {
                hl: "en"
            }
        } // Make options for the search

        const responces = await google.search(msg.content.substring(prefix.length + "search".length), options) // Search for the query
        const firstresponce = responces.results[0] // Get the first responce of the search

        const embed = new Discord.MessageEmbed()
            .setTitle("Search results")
            .setDescription("Query: " + msg.content.substring(prefix.length + "search".length))
            .addField("Search result:", firstresponce.title + "\nUrl: " + firstresponce.url) // Make the embed with the first responce's url and title

        message.edit({embeds: [embed], content: "Found!"}) // Edit the message so people see the query
    }
}

module.exports = {useCommands} // Export our command
