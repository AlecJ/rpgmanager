import React from 'react'
import styles from './styles/SlideInDiv.module.scss'

export default (props) => {
    const { show, style, fromDirection, children } = props

    /*
    This component hides elements off screen and then has them slide in when enabled.

    Props:
    Direction decides which way the element slides in from.

    Time for the animation to slide the container in.

    Size

    Final position
    */

    // const slideFromDirection = (!!fromDirection && fromDirection) || 'left'
    // const className = `${styles.container} ${styles[`${slideFromDirection}`]}`

    // translate into left and top
    
    const paddingTop = style.top
    
    // height can be % or vh
    var height = style.height
    if (height.includes('%')) {
        height = +height.replace('%', '') + +paddingTop.replace('%', '')
        height = height + "%"
    } else if (height.includes('vh')) {
        height = +height.replace('vh', '') + +paddingTop.replace('vh', '')
        height = height + "%"
    }

    const showStyle = {...style, top: null, paddingTop: paddingTop, height: height}
    const innerStlye = {...style, top: null, height: '100%', width: '100%', padding: null}

    const hideStyle = fromDirection === 'top' ? {...style, top: 0, height: 0} :
                      fromDirection === 'bottom' ? {...style, top: '100vh', height: 0} :
                      fromDirection === 'right' ? {...style,
                                                   top: null,
                                                   paddingTop: paddingTop, 
                                                   height: height,
                                                   left: '100%',
                                                   right: null,
                                                   width: 0} :
                      // else left
                      {...style,
                       top: null,
                       paddingTop: paddingTop,
                       height: height,
                       left: null,
                       right: '100vw',
                       width: 0}
  

    return (
        <div
            className={styles.container}
            style={!!show && show ? showStyle : hideStyle}
        >
            <div style={innerStlye}>
                {children}
            </div>
        </div>
    )
}
