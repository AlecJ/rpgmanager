import React from 'react'
import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form'
import ClassDropDown from './ClassDropdown'

import ToggleMouseOver from '../common/util/ToggleMouseOver'

import styles from './styles/Party.module.scss'

export default (props) => {
    const { character, ratio, handleChange, calcMoney, deleteCharacter } = props
    const { name, items, notes, gold, silver, copper, dGold, dSilver, dCopper } = character

    const charClass = !!character.role ? character.role : 'missing'
    const classPic = <div className={`${styles.classPic} ${styles[`${charClass}`]}`}></div>

    return (
        <div>
            <div className={styles.playerContainer}>
                <div className={styles.playerName}>
                    <textarea
                        className={styles.formControl}
                        spellCheck={'false'}
                        maxLength={22}
                        name='name'
                        onChange={handleChange}
                        value={!!name ? name : ''}
                        placeholder={'Name...'}
                    />
                </div>
                <div className={styles.playerPic}>
                    <ToggleMouseOver
                        defaultContent={classPic}
                        mouseOverContent={<ClassDropDown handleChange={handleChange} />}
                    />
                </div>
                <div className={styles.playerMoney}>
                    <div className={styles.currencyIcons}>
                        <div className={styles.gold}>
                            <div className={styles.goldIcon} />
                        </div>
                        <div>
                            <div className={styles.silverIcon} />
                        </div>
                        <div>
                            <div className={styles.copperIcon} />
                        </div>
                    </div>
                    <div className={styles.currentMoney}>
                        <Form.Control
                            className={styles.gold}
                            name='gold'
                            onChange={handleChange}
                            value={!!gold ? gold : 0}
                            maxLength={4}
                        />
                        <Form.Control
                            className={styles.silver}
                            name='silver'
                            onChange={handleChange}
                            value={!!silver ? silver : 0}
                            maxLength={!!ratio && ratio === 10 ? 1 : 2}
                        />
                        <Form.Control
                            className={styles.copper}
                            name='copper'
                            onChange={handleChange}
                            value={!!copper ? copper : 0}
                            maxLength={!!ratio && ratio === 10 ? 1 : 2}
                        />
                    </div>
                    <div className={styles.deltaMoney}>
                        <Form.Control
                            className={styles.gold}
                            name='dGold'
                            onChange={handleChange}
                            value={!!dGold ? dGold : ''}
                            maxLength={4}
                        />
                        <Form.Control
                            className={styles.silver}
                            name='dSilver'
                            onChange={handleChange}
                            value={!!dSilver ? dSilver : ''}
                            maxLength={!!ratio && ratio === 10 ? 1 : 2}
                        />
                        <Form.Control
                            className={styles.copper}
                            name='dCopper'
                            onChange={handleChange}
                            value={!!dCopper ? dCopper : ''}
                            maxLength={!!ratio && ratio === 10 ? 1 : 2}
                        />
                        <Button
                            onClick={() => calcMoney(true)}
                            className={styles.calcBtn}
                            variant='success'
                        >
                            <img src='/assets/open-iconic/svg/plus.svg' alt='icon name' />
                        </Button>
                        <Button
                            onClick={() => calcMoney(false)}
                            className={styles.calcBtn}
                            variant='danger'
                        >
                            <img src='/assets/open-iconic/svg/minus.svg' alt='icon name' />
                        </Button>
                    </div>
                </div>
                <div className={styles.playerItems}>
                    <p>Items</p>
                    <textarea
                        className={styles.formControl}
                        spellCheck={'false'}
                        name='items'
                        onChange={handleChange}
                        style={{ fontSize: '16px' }}
                        value={!!items ? items : ''}
                        placeholder={'Items...'}
                    />
                </div>
                <div className={styles.playerNotes}>
                    <p>Notes</p>
                    <textarea
                        className={styles.formControl}
                        spellCheck={'false'}
                        name='notes'
                        onChange={handleChange}
                        style={{ fontSize: '16px' }}
                        value={!!notes ? notes : ''}
                        placeholder={'Notes...'}
                    />
                </div>
            </div>
            <div className={styles.playerDelete}>
                <Button onClick={deleteCharacter} variant='danger'>
                    <img src='/assets/open-iconic/svg/trash.svg' alt='icon name' />
                </Button>
            </div>
        </div>
    )
}
