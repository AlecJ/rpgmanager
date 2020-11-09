import React from 'react'
import Button from 'react-bootstrap/Button'
import PlayerCard from './PlayerCard'

import styles from './styles/Party.module.scss'

export default (props) => {
    const {
        campaign,
        createCharacter,
        handleCharacterChange,
        calcMoney,
        deleteCharacter,
    } = props

    const { characters, money_ratio } = campaign
    const playerCards = characters
        .slice()
        .reverse()
        .map((c, i) => {
            return (
                <PlayerCard
                    key={'player_' + i}
                    character={c}
                    ratio={money_ratio}
                    handleChange={handleCharacterChange(c.id)}
                    calcMoney={calcMoney(c.id)}
                    deleteCharacter={deleteCharacter(c.id)}
                />
            )
        })

    return (
        <div className={styles.container}>
            <div className={styles.scrollContainer}>
                {playerCards}

                {playerCards.length < 6 ? (
                    <div className={styles.addPlayerButtonContainer}>
                        <Button
                            onClick={createCharacter}
                            variant='secondary'
                            className={styles.addPlayerButton}
                        >
                            <img src='/assets/open-iconic/svg/plus.svg' alt='icon name' />
                        </Button>
                    </div>
                ) : null}
            </div>
        </div>
    )
}
