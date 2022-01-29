const Discord = require("discord.js")
const mathutils = require("../mathutils")

function useCommands(msg, prefix) {
    if (msg.content.toLowerCase().startsWith(prefix + "eightball")) { // Check if the message starts with the prefix and eightball so users can use the command
        const ballresponce = [
            "Yes", "No", "Take a wild guess...", "Very doubtful",
            "Sure", "Without a doubt", "Most likely", "Might be possible",
            "You'll be the judge", "No... (╯°□°）╯︵ ┻━┻", "No!",
            "bruh no","Maybe, 👀","gg","I don't know"
        ] // Tells our program what answers we want from the bot

        const answer = ballresponce[mathutils.getRandomInt(0, ballresponce.length - 1)] // Gets a random answer from the responces section

        msg.channel.send(answer) // Sends the answer (when I ask if I am a good person it always says no (Yaumama writing) )
    }

    if (msg.content.toLowerCase().startsWith(prefix + "hotlevel")) { // Check if the message is the prefix and hotlevel
        const hot = mathutils.getRandomInt(0, 100) // Get the percentage of hot the person is
        let emoji // Make an unsigned variable for us to set later

        if (hot > 75) { // Check if the hot level is above these levels and add emojis accordingly
            emoji = "💞"
        } else if (hot > 50) {
            emoji = "💖"
        } else if (hot > 25) {
            emoji = "❤"
        } else {
            emoji = "💔"
        }

        msg.channel.send("**" + msg.member.displayName + "** is " + hot + "% hot! " + emoji) // Send the hot level and emoji
    }
}

module.exports = {useCommands}
