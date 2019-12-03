$(document).ready(function() {  // Load all html elems before adding evt handlers
    const tracksBtn = $('.tracks-btn');

    // Get tracks from a playlist and display in a modal
    tracksBtn.on('click', (evt) => {
        evt.preventDefault();
        const playlistId = evt.target.value;
        console.log(playlistId);

        // Get playlist tracks and add to modal div
        $.get('/playlist-tracks', {'pl':playlistId}, (tracks) => {
            for (track of tracks) {
                $(`.modal-${playlistId} ol`).append(`<li><a href="/tracks/${track.track_id}">${track.artist} - ${track.track_name}</a></li>`);
            }
        });
    });


    // Remove track from page when user clicks X
    const deselectBtn = $('.deselect');
    deselectBtn.on('click', (evt) => {
        evt.preventDefault();
        const trackId = evt.target.value;
        $(`#deselect-${trackId}-div`).remove();
    });


    // Submit new playlist
    const createPlaylistBtn = $('#create-pl');
    createPlaylistBtn.on('click', (evt) => {
        evt.preventDefault();

        trackIds = [];
        const plName = $('#new-pl-name').html();  // Get playlist name
        const trackDivs = $('.add-track-div');  // Get tracks

        // Store track ids in array
        for (const track of trackDivs) {
            trackIds.push(track.getAttribute('value'));
        };

        console.log(trackIds);
        if (trackIds != [] && plName != '') {
            // Create dict object to pass to add-playlist route
            let newPl = {'pl_name': plName,
                        'tracks': trackIds};

            // Add playlist to db
            $.post('/add-playlist', newPl, (res) => {
                alert(`${plName} has been created.`);
            });
        }
    });
})