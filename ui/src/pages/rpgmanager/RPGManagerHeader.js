import React from 'react'
import Form from 'react-bootstrap/Form'
import Spinner from 'react-bootstrap/Spinner'
import Button from 'react-bootstrap/Button'
import styles from './styles/RPGManagerHeader.module.scss'

export default (props) => {
    const { handleChange, toggleNotes, campaign, isSaving } = props
    const { name, region, day, party_level, money_ratio } = campaign

    return (
        <div className={styles.container}>
            <div className={styles.left}>
                <div className={styles.title}>
                    <Form.Control
                        name='name'
                        onChange={handleChange}
                        style={{ fontSize: '28px' }}
                        value={!!name ? name : ''}
                        placeholder={'Campaign Title'}
                    />
                </div>
                <div className={styles.inlineTextInput}>
                    <div className={styles.inlineTextInputLabel}>
                        <p>Current Location</p>
                    </div>
                    <div className={styles.inlineTextInputField}>
                        <Form.Control
                            name='region'
                            onChange={handleChange}
                            value={!!region ? region : ''}
                            placeholder={'Location Name'}
                        />
                    </div>
                </div>
            </div>
            <div className={styles.right}>
                {!!isSaving && isSaving ? (
                    <div className={styles.loading}>
                        <Spinner animation='border' size='sm' />
                    </div>
                ) : null}
                <div className={styles.inlineTextInput}>
                    <div className={styles.inlineTextInputLabel}>
                        <p>Day</p>
                    </div>
                    <div className={styles.inlineTextInputField} style={{ width: '60px' }}>
                        <Form.Control
                            name='day'
                            onChange={handleChange}
                            value={!!day ? day : 1}
                            maxLength={4}
                        />
                    </div>
                </div>
                <div className={styles.inlineTextInput}>
                    <div className={styles.inlineTextInputLabel}>
                        <p>Party Level</p>
                    </div>
                    <div className={styles.inlineTextInputField} style={{ width: '60px' }}>
                        <Form.Control
                            name='party_level'
                            onChange={handleChange}
                            value={!!party_level ? party_level : 1}
                            maxLength={2}
                        />
                    </div>
                </div>
                <div className={styles.inlineTextInput}>
                    <div className={styles.inlineTextInputLabel}>
                        <p>Currency: Use x10</p>
                    </div>
                    <div>
                        <Form.Check
                            id='money_ratio'
                            type='switch'
                            label=''
                            checked={!!money_ratio ? money_ratio === 100 : false}
                            name='money_ratio'
                            onChange={handleChange}
                        />
                    </div>
                    <div className={`${styles.postInlineTextInputLabel}`}>
                        <p>Use x100</p>
                    </div>
                </div>
            </div>
            <div className={styles.notesButtonContainer}>
                <Button
                    onClick={toggleNotes}
                    variant='outline-secondary'
                    className={styles.notesButton}
                >
                    <img src='/assets/open-iconic/svg/book.svg' alt='icon name' />
                </Button>
            </div>
        </div>
    )
}
