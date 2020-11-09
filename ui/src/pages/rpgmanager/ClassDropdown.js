import React from 'react'
import Dropdown from 'react-bootstrap/Dropdown'
import DropdownButton from 'react-bootstrap/DropdownButton'

export default (props) => {
    const { handleChange } = props

    return (
        <DropdownButton title='Select Class' rootCloseEvent='click'>
            <Dropdown.Item
                onClick={() => handleChange({ target: { name: 'role', value: 'barbarian' } })}
            >
                Barbarian
            </Dropdown.Item>
            <Dropdown.Item
                onClick={() => handleChange({ target: { name: 'role', value: 'bard' } })}
            >
                Bard
            </Dropdown.Item>
            <Dropdown.Item
                onClick={() => handleChange({ target: { name: 'role', value: 'cleric' } })}
            >
                Cleric
            </Dropdown.Item>
            <Dropdown.Item
                onClick={() => handleChange({ target: { name: 'role', value: 'druid' } })}
            >
                Druid
            </Dropdown.Item>
            <Dropdown.Item
                onClick={() => handleChange({ target: { name: 'role', value: 'fighter' } })}
            >
                Fighter
            </Dropdown.Item>
            <Dropdown.Item
                onClick={() => handleChange({ target: { name: 'role', value: 'monk' } })}
            >
                Monk
            </Dropdown.Item>
            <Dropdown.Item
                onClick={() => handleChange({ target: { name: 'role', value: 'paladin' } })}
            >
                Paladin
            </Dropdown.Item>
            <Dropdown.Item
                onClick={() => handleChange({ target: { name: 'role', value: 'ranger' } })}
            >
                Ranger
            </Dropdown.Item>
            <Dropdown.Item
                onClick={() => handleChange({ target: { name: 'role', value: 'rogue' } })}
            >
                Rogue
            </Dropdown.Item>
            <Dropdown.Item
                onClick={() => handleChange({ target: { name: 'role', value: 'sorcerer' } })}
            >
                Sorcerer
            </Dropdown.Item>
            <Dropdown.Item
                onClick={() => handleChange({ target: { name: 'role', value: 'warlock' } })}
            >
                Warlock
            </Dropdown.Item>
            <Dropdown.Item
                onClick={() => handleChange({ target: { name: 'role', value: 'wizard' } })}
            >
                Wizard
            </Dropdown.Item>
        </DropdownButton>
    )
}
