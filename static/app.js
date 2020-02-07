$(document).ready(function() {  // Load all html elems before adding evt handlers
    const tracksBtn = $('.tracks-btn');
    // Get tracks from a playlist and display in a modal
    tracksBtn.on('click', (evt) => {
        evt.preventDefault();
        const playlistId = evt.target.value;

        // Get playlist tracks and add to modal div
        $.get('/playlist-tracks', {'pl':playlistId}, (tracks) => {
            for (track of tracks) {
                $(`.modal-${playlistId} ol`).append(`<li><a href="/tracks/${track.track_id}">${track.artist} - ${track.track_name}</a></li>`);
            }
        });

        // Display modal
        $(`#exampleModalLong-${playlistId}`).modal('show');
    });


    const trackDtlBtn = $('.track-dtl-btn');
    // Get track information and display in a modal
    trackDtlBtn.on('click', (evt) => {
        evt.preventDefault();
        const trackId = evt.target.value;

        // Get track details and add to modal div
        $.get('/track-detail', {'track':trackId}, (track) => {
            guts = `<strong>Artist:</strong> ${track.artist}
                    <br><strong>Duration:</strong> ${track.duration}
                    <br><strong>BPM:</strong> ${track.tempo}
                    <br><strong>Key:</strong> ${track.key}
                    <br><strong>Danceability:</strong> ${track.danceability}
                    <br><strong>Valence:</strong> ${track.valence}`
            $(`.modal-${trackId}-body`).html(`${guts}`);
        });

        // Display modal
        $(`#exampleModalLong-${trackId}`).modal('show');
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
                window.location.href = '/playlists';
            });
        }
    });
})