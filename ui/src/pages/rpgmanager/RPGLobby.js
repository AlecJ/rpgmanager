import React from 'react'
import Button from 'react-bootstrap/Button'
import styles from './styles/RPGLobby.module.scss'

export default (props) => {
    const { roomCode, loadFailed, createGame } = props

    return (
        <div className={styles.container}>
            <h2>Create a New Campaign</h2>

            <p>
                If you already have a campaign, enter the room code into <br />
                the browser. Like "/rpgmanager/YOUR_ROOM_CODE"
            </p>

            {loadFailed ? (
                <p className={styles.errorText}>
                    Could not find a campaign with the code: {roomCode}
                </p>
            ) : null}

            <Button onClick={createGame} variant='primary'>
                Create New Campaign
            </Button>
        </div>
    )
}
