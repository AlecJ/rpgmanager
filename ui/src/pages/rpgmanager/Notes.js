import React from 'react'
import styles from './styles/Notes.module.scss'

export default (props) => {
    const { handleChange, campaign } = props

    const notes = !!campaign && !!campaign.notes ? campaign.notes : ''

    return (
        <div className={styles.notes}>
            <h2>Notes</h2>
            <textarea
                className={styles.formControl}
                spellCheck={'false'}
                name='notes'
                onChange={handleChange}
                style={{ fontSize: '16px' }}
                value={!!notes ? notes : ''}
            />
        </div>
    )
}
