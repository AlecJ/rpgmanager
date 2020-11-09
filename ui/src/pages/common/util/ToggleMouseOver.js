import React, { Component } from 'react'

class ToggleMouseOver extends Component {
    constructor(props) {
        super(props)

        this.state = {
            mouseIsOver: true,
        }

        this.toggleClassDropdown = this.toggleClassDropdown.bind(this)
    }

    componentDidMount() {
        this.toggleClassDropdown(false)
    }

    toggleClassDropdown(val) {
        this.setState({ mouseIsOver: val })
    }

    render() {
        const { mouseOverContent, defaultContent } = this.props
        const { mouseIsOver } = this.state

        const containerStyle = { width: '100%', height: '100%', position: 'relative' }

        const defaultStyle = {
            width: '100%',
            height: '100%',
        }

        const fadeStyle = {
            position: 'absolute',
            width: '100%',
            height: '100%',
            opacity: '0.5',
        }

        const mouseOverStyle = {
            position: 'absolute',
            width: '100%',
            height: '100%',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
        }

        return (
            <div
                style={defaultStyle}
                onMouseOver={() => this.toggleClassDropdown(true)}
                onMouseLeave={() => this.toggleClassDropdown(false)}
            >
                {mouseIsOver ? (
                    <div style={containerStyle}>
                        <div style={fadeStyle}>{defaultContent}</div>
                        <div style={mouseOverStyle}>{mouseOverContent}</div>
                    </div>
                ) : (
                    <div style={defaultStyle}>{defaultContent}</div>
                )}
            </div>
        )
    }
}

export default ToggleMouseOver
