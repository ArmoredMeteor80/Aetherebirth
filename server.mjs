import net from "net";

const PORT = 5555;

let id = 0;

const players = {};

const server = net.createServer((socket) => {
    console.log("Connected");
    const player = {
        id: id,
        receivedData: {},
        sentDataCache: {},
    }
    players[player.id] = player;
    
    socket.write(JSON.stringify(player));
    id++;

    socket.on("data", (data) => {
        const receivedData = JSON.parse(data);
        player.receivedData = receivedData;

        const sameMapPlayers = [];
        for(const playerId of Object.keys(players)) {
            if((player.id != players[playerId].player_number) && (players[playerId]?.receivedData?.position?.map == player?.receivedData?.position?.map)){
                let tData = players[playerId].receivedData;
                tData.id = playerId;
                sameMapPlayers.push(tData);
            }
        }

        if(JSON.stringify(sameMapPlayers) != JSON.stringify(player.sentDataCache.players)){
            player.sentDataCache = {id:player.player_number, players: sameMapPlayers};
            socket.write(JSON.stringify(player.sentDataCache));
        } else {
            socket.write(JSON.stringify({id:player.player_number, changed: false}))
        }
    });

    socket.on("close", (hadError) => {
        if(hadError) console.log(`Connection with player ${player.id} lost`);
        else console.log(`Player ${player.id} disconnected`)
        delete players[player.id]
    })
    
}).listen(PORT);

